function formedit(event, id) {
    event.preventDefault();
    document.getElementById(`editform${id}`).style.display = 'block';
        
}

function sendedit(event, id){
    event.preventDefault();
    let post_id = document.getElementById(`editid${id}`).value;
    let post_content = document.getElementById(`editcontent${id}`).value;
    const myInit = {
        method: 'PUT',
        body: JSON.stringify({
            "id": post_id,
            "content": post_content
        })
    }
    fetch("/edit", myInit)
    .then(response => response.json())
    .then(result => {
        document.getElementById(`editform${result['id']}`).style.display = 'none';
        document.getElementById(`content${result['id']}`).innerHTML = result['content'];
        console.log(result);
    })
}

function likepost(event, id){
    event.preventDefault();
    const myInit = {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    }
    fetch("/like", myInit)
    .then(response => response.json())
    .then(result => {
        document.getElementById(`length${id}`).innerHTML = result['likes'];
        let temp = document.getElementById(`likepost${id}`);
        temp.innerHTML = "Unlike";
        temp.id = `unlikepost${id}`;
        temp.setAttribute("onclick", `unlikepost(event, ${id})`);
    })
}

function unlikepost(event, id){
    event.preventDefault();
    const myInit = {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    }
    fetch("/unlike", myInit)
    .then(response => response.json())
    .then(result => {
        document.getElementById(`length${id}`).innerHTML = result['likes'];
        let temp = document.getElementById(`unlikepost${id}`);
        temp.innerHTML = "Like";
        temp.id = `likepost${id}`;
        temp.setAttribute("onclick", `likepost(event, ${id})`);
    })
}

function follow(event, id){
    event.preventDefault();
    const myInit = {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    }
    fetch("/follow", myInit)
    .then(response => response.json())
    .then(result => {
        document.getElementById(`followers${id}`).innerHTML = result['followers'];
        let temp = document.getElementById(`follow${id}`);
        temp.innerHTML = "Unfollow";
        temp.id = `unfollow${id}`;
        temp.setAttribute("onclick", `unfollow(event, ${id})`);
    })
}

function unfollow(event, id){
    event.preventDefault();
    const myInit = {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    }
    fetch("/unfollow", myInit)
    .then(response => response.json())
    .then(result => {
        document.getElementById(`followers${id}`).innerHTML = result['followers'];
        let temp = document.getElementById(`unfollow${id}`);
        temp.innerHTML = "Follow";
        temp.id = `follow${id}`;
        temp.setAttribute("onclick", `follow(event, ${id})`);
    })
}
