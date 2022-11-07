let dropdown = document.getElementById("dropdown")
dropdown.addEventListener('click', () => {
    let sideBarHeadingListP = document.querySelectorAll('.sideBarHeadingListP')
    let sideBar = document.querySelector('.sideBar')
    sideBar.classList.toggle('active')
    sideBarHeadingListP.forEach((item) => {
        item.classList.toggle('active')
    })
})

let libraryDrop = document.getElementById('libraryDrop')
libraryDrop.addEventListener('click', () => {
    let mobileBar = document.querySelector('.mobileBar')
    mobileBar.classList.toggle('active')
})

// function like(){
    
// }
// $(document).on('click', '#ajax_like', function (e){
//     e.preventDefault();
//     $.ajax({
//         type:'POST',
//         url: '{%url "like" film.id %}',
//         data:{
//             postid: $('#ajax_like').val(),
//             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//             action: 'post'
//         },
//         success: function (json){
//             document.getElementById('like_result').innerHTML = json['like_result']
//             console.log(json)
//         },
//         error: function (xhr, errmsg, err){

//         }
//     });
// })