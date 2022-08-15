import random
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Category
from .forms import MovieCreateForm
from django.views.generic.edit import DeleteView
from moviepy.editor import *


def index(request):
    movs = Movie.objects.all()[:3]
    data = {
        'movs': movs
    }
    return render(request, 'index.html', data)

def modal(request):
    return render(request, 'video_modal.html', {})

def create_movie(request):
    if not request.user.id:
        return render(request, 'blank.html', {})
    def convert(seconds):
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return f'{mins}:{seconds}'

    if request.method == 'POST':
        val_error = False
        if ValidationError:
            val_error = True
        form = MovieCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)# This allows us to insert the user as the uploader of the movie
            obj.uploader = request.user
            vid = request.FILES['movie']
            try:
                clip = VideoFileClip(vid.temporary_file_path())
                temp_length = int(clip.duration)
                            
                if temp_length > 600:
                    length_error = 'Film Is Longer Than 15 Minutes'
                    return render(request, 'add_movie.html', {'form':form,'length_error':length_error})
                elif temp_length <= 600:
                    obj.length = convert(int(clip.duration))
                    obj.save()
                    # succes = 'Your Movie Was Uploaded Succesfully'
                    return redirect('dashboard', request.user.id)
            except:
                clip = random.randint(1,15)
                temp_length = int(clip)

                if temp_length > 600:
                    length_error = 'Film Is Longer Than 15 Minutes'
                    return render(request, 'add_movie.html', {'form':form,'length_error':length_error})
                elif temp_length <= 600:
                    obj.length = convert(int(temp_length))
                    obj.save()
                    # succes = 'Your Movie Was Uploaded Succesfully'
                    return redirect('dashboard', request.user.id)

    else:
        form = MovieCreateForm()
        val_error = False
    return render(request, 'add_movie.html', {'form':form, 'validation_error': 'Not A Valid File Type', 'val_error':val_error})

def dashboard(request, pk):
    if request.user.id != pk:
        permission_error = 'You Have No Permission To Be Here !!!'
        return render(request, 'dashboard.html', {'permission_error':permission_error})
    # elif not request.user.id:
    #     permission_error = 'You Have No Permission To Be Here !!!'
    #     return render(request, 'dashboard.html', {'permission_error':permission_error})
    film = Movie.objects.all().order_by('-upload_date')
    cats = Category.objects.all()
    data = {
        'film': film,
        'cats': cats,
    }
    return render(request, 'dashboard.html', data)

def movie_detail(request, pk):
    if not request.user.id:
        return render(request, 'blank.html', {})
    favs = Movie.objects.filter(favourites=request.user)
    mov_for_you = Movie.objects.all().order_by('-upload_date')
    mov = Movie.objects.get(id=pk)
    if mov in favs:
        fav = True
    else:
        fav = False
    collect_likes = get_object_or_404(Movie, id=pk)
    liked = False
    disliked = False
    if collect_likes.likes.filter(id=request.user.id).exists():
        liked = True
    total_likes = collect_likes.total_likes()
    if collect_likes.dislikes.filter(id=request.user.id).exists():
        disliked = True
    total_dislikes = collect_likes.total_dislikes()
    data = {
        'film': mov,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'liked': liked,
        'movies_for_you': mov_for_you,
        'fav':fav,
    }
    return render(request, 'video_modal.html', data)

def list_movie(request):
    
    film = Movie.objects.all()
    data = {
        'film': film,
    }
    return render(request, 'list_movie.html', data)

def add_favourite(request, id):
    film = get_object_or_404(Movie, id=id)
    user = request.user
    if film.favourites.filter(id=request.user.id).exists():
        film.favourites.remove(request.user)
        return redirect('detail', id)
    else:
        film.favourites.add(request.user)
        return redirect('detail', id)
    return redirect('library')

# def list_favourites(request):
#     favs = Movie.objects.filter(favourites=request.user)
#     return render(request, 'favourites.html', {'favs':favs})



def delete(request, pk):
    if not request.user.id:
        return render(request, 'blank.html', {})
    mov = Movie.objects.get(id=pk)
    mov.delete()
    return redirect('my_videos')
    
def add_likes(request, pk):
    post = get_object_or_404(Movie, id=pk)
    print(post)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        
    else:
        post.likes.add(request.user)
        liked = True
        

    return redirect('detail', pk)

def add_dislikes(request, pk):
    post = get_object_or_404(Movie, id=pk)
    print(post)
    disliked = False

    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
        
    else:
        post.dislikes.add(request.user)
        disliked = True
        

    return redirect('detail', pk)

def my_movies(request):
    if not request.user.id:
        return render(request, 'blank.html', {})
    if not request.user:
        permission_error = "You Don't Have Permission To View This Page"
        return render(request, 'my_movies.html', {'permission_error':permission_error})
    favs = Movie.objects.filter(favourites=request.user)
    movs = Movie.objects.filter(uploader=request.user)
    cats = Category.objects.all()
    data = {
        'movs':movs,
        'favs':favs,
        'cats':cats
        }
    return render(request, 'library.html', data)

def terms(request):
    return render(request, 'terms.html', {})

def settings(request):
    if not request.user.id:
        return render(request, 'blank.html', {})
    return render(request, 'settings.html', {})

def my_videos(request):
    if not request.user.id:
        return render(request, 'blank.html', {})
    movs = Movie.objects.filter(uploader=request.user)
    data = {
        'movs':movs
    }
    return render(request, 'my_videos.html', data)