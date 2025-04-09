document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.getElementById('compose-form').addEventListener('submit', (event) => {
    event.preventDefault();
    send_email();
  });
  
  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //get the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then((result) => {
    console.log(result);
    result.forEach(element => {
      let newdiv = document.createElement('div');
      newdiv.setAttribute('class', 'box');
      let id = element['id'];
      let sender = element['sender'];
      let subject = element['subject'];
      let timestamp = element['timestamp'];
      newdiv.innerHTML = `<strong>sender</strong>: ${sender} <br> <strong>subject</strong>: 
                          ${subject} <br> <strong>timestamp</strong>: ${timestamp}`;
      if(element['read']){
        newdiv.style = 'background-color: gray; color: white;';
      }
      document.getElementById('emails-view').appendChild(newdiv);
      newdiv.addEventListener('click', () => view_email(id));
    });
  });
}

function send_email() {
  compose_recipients = document.getElementById('compose-recipients').value;
  compose_subect = document.getElementById('compose-subject').value;
  compose_body = document.getElementById('compose-body').value;
  myInit = {
    method: "POST",
    body: JSON.stringify({
      recipients: compose_recipients,
      subject: compose_subect,
      body: compose_body
    })
  }
  fetch('/emails', myInit)
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  });
}

function view_email(id) {
  myInit = {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  };
  fetch(`/emails/${id}`, myInit);

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(result => {
    document.getElementById('emails-view').style.display = 'None';
    document.getElementById('email-view').style.display = 'block';
    let currentemail = document.getElementById('useremail').innerHTML;
    if (currentemail == result['sender']){
      var buttontext = ``;
    }
    else{
      var buttontext = `<button id='reply' class='btn btn-primary'>Reply</button>`;
    }

    if (result['archived']){
      var archivetext = `<button id='unarchive' class='btn btn-primary'>Unarchive</button>`;
    }
    else{
      var archivetext = `<button id='archive' class='btn btn-primary'>Archive</button>`;
    }
    document.getElementById('email-view').innerHTML = `<strong>From</strong>: ${result['sender']} <br>
                                                        <strong>To</strong>: ${result['recipients'].toString()} <br>
                                                        <strong>Subject</strong>: ${result['subject']} <br>
                                                        <strong>Timestamp</strong>: ${result['timestamp']} <br>` +
                                                        buttontext + archivetext +
                                                         `<br>
                                                        <p style='margin-top: 1em;'>${result['body']}</p>`;
   document.getElementById('reply').addEventListener('click', function(){
      compose_email();
      if(result['subject'].charAt(0) == 'R' && result['subject'].charAt(1) == 'e' && result['subject'].charAt(2) == ':'){
        document.getElementById('compose-subject').value = `${result['subject']}`;  
      }
      else{
        document.getElementById('compose-subject').value = `Re: ${result['subject']}`;
      }
      document.getElementById('compose-body').value = `On ${result['timestamp']} ${result['sender']} wrote: ${result['body']}\n\n`;
      document.getElementById('compose-recipients').value = `${result['sender']}`;
   });
   if (result['archived']){
    document.getElementById('unarchive').addEventListener('click', () => unarchive(id));
   }
   else{
    document.getElementById('archive').addEventListener('click', () => archive(id));
   }
  })
}

function archive(id) {
myInit = {
  method: 'PUT',
  body: JSON.stringify({
    archived: true
  })
}
fetch(`/emails/${id}`, myInit)
.then(() => {
  load_mailbox('archive');
})
}

function unarchive(id) {
  myInit = {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  }
  fetch(`/emails/${id}`, myInit)
  .then(() => {
    load_mailbox('archive');
  })
  }