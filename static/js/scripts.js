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
                Like(this.id.substring(8), false)
                this.classList.remove('btn-primary')
                this.classList.add('btn-secondary')
                this.textContent = 'Dislike'
            }
            else{
                Like(this.id.substring(8), true)
                this.classList.remove('btn-secondary')
                this.classList.add('btn-primary')
                this.textContent = 'Like'
            }
            updatePostData(this.id.substring(8))
        })
    }
    if(document.getElementById('discard_btn')){
        document.getElementById('discard_btn').addEventListener('click', (e) => {
            e.preventDefault()
            clear()
        })
    }
    if(document.getElementById('add_post')){
        document.getElementById('add_post').addEventListener('click', getFiles)
    }
})

function getFiles(){
    title = document.getElementById('Title')
    tags = document.getElementById('tags')
    Imagefile = document.getElementById('Poster')
    content = document.getElementById('Content')
    console.log(Imagefile.files[0])
    formData = new FormData()
    formData.append('image', Imagefile.files)
    formData.append('Title', title.value)
    formData.append('tags', tags.value)
    formData.append('content', content.value)
    $.ajax({ 
        url: '/AddPost', 
        method: 'POST', 
        data: formData,
        cache:false, 
        processData: false, 
        contentType: false, 
        success: function (data) {                       
            console.log('sucess')
        }, 
        error: function (xhr, status, error) {                        
            console.error(error); 
        } 
    });
}

function Like(Post_id, delete_like){
    console.log(Post_id)
    formData = new FormData();
    formData.append('post_ID', String(Post_id))
    formData.append('Delete', delete_like)
    $.ajax({ 
        url: '/Posts', 
        method: 'POST', 
        data: formData,
        cache:false, 
        processData: false, 
        contentType: false, 
        success: function (data) {                       
            document.getElementById('postlikes_'+Post_id).textContent = data.likes[0][0]
        }, 
        error: function (xhr, status, error) {                        
            console.error(error); 
        } 
    });
}

function updatePostData(Post_id) {
    $.ajax({
        url: `/UpdatePosts/${Post_id}`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            document.getElementById('postlikes_'+Post_id).textContent = data.likes[0][0]
        },
        error: function() {
            console.error('Error fetching data.');
        }
    });
}

function clear(){
    document.getElementById('comment_sect').value = '';
}