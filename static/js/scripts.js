/*!
* Start Bootstrap - Blog Post v5.0.9 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/

window.addEventListener('load', (e) =>{
    buttons = document.getElementsByClassName('LikeButton');
    for(idx = 0; idx < buttons.length; idx++){
        buttons[idx].addEventListener('click', function(e){
            if(this.classList.contains('btn-primary')){
                Like(this.id[8], false)
                this.classList.remove('btn-primary')
                this.classList.add('btn-secondary')
                this.textContent = 'Dislike'
            }
            else{
                Like(this.id[8], true)
                this.classList.remove('btn-secondary')
                this.classList.add('btn-primary')
                this.textContent = 'Like'
            }
        })
    }
})

function Like(Post_id, delete_like){
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", "?like", true);
    data = new FormData();
    data.append('post_ID', String(Post_id))
    data.append('Delete', delete_like)
    xhttp.send(data);
}