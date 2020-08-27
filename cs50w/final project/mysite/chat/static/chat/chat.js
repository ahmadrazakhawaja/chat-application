document.addEventListener('DOMContentLoaded', function() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }



// index page js
if(document.querySelector('#room-name-input')!=null){
    document.querySelector('#room-name-input').focus();
    document.querySelector('#room-name-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#room-name-submit').click();
        }
    }
    

    document.querySelector('#room-name-submit').onclick = function(e) {
        var roomName = document.querySelector('#room-name-input').value;
    

    fetch('/addcontact', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#room-name-input').value,
        }),
        headers: { "X-CSRFToken": getCookie('csrftoken')}
      })
      .then(response => {
        if(response.status===201){
           lol = 1;
           return response.json();
        }
        else{
          lol = 2;
          return response.json();
        }
      })
      .then(result => {
            if(result.message==='Contact added'){
                    //const elementx = document.createElement('div');
                    //elementx.className="contacts";
                //elementx.innerHTML = ` Username: ${document.querySelector('#room-name-input').value} <br> Status: ${result.status}`;
                //document.querySelector('.grid-container').append(elementx);
                window.location.pathname = '/contact/' + result.room_namex + '/';
            }
            else if(result.message==='Username doesnot exist'){
                return false;
            }
          
          console.log(result);
      })
    };
}
      

if(document.querySelector('#group-name-input')!=null){
    document.querySelector('#group-name-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#group-name-submit').click();
        }
    }
    

    document.querySelector('#group-name-submit').onclick = function(e) {
        var roomName = document.querySelector('#group-name-input').value;
    

    fetch('/group', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#group-name-input').value,
        }),
        headers: { "X-CSRFToken": getCookie('csrftoken')}
      })
      .then(response => {
        if(response.status===201){
           lol = 1;
           return response.json();
        }
        else{
          lol = 2;
          return response.json();
        }
      })
      .then(result => {
            if(result.message==='Group created'){
                window.location.pathname = '/contact/' + result.group_name + '/';
            }
            else if(result.message==='Group name taken please choose a new name.'){
                return false;
            }
          
          console.log(result);
      })
    };
}
      
if(document.querySelector('#group-member-input')!=null){
    document.querySelector('#group-member-input').focus();
    document.querySelector('#group-member-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#group-member-submit').click();
        }
    }
    

    document.querySelector('#group-member-submit').onclick = function(e) {
        var roomName = document.querySelector('#group-member-input').value;
    
    fetch('/addgroup', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#group-member-input').value,
            channel: document.querySelector('#room-name').innerHTML
        }),
        headers: { "X-CSRFToken": getCookie('csrftoken')}
      })
      .then(response => {
        if(response.status===201){
           lol = 1;
           return response.json();
        }
        else{
          lol = 2;
          return response.json();
        }
      })
      .then(result => {
            if(result.message==='member added'){
                    const elementx = document.createElement('div');
                    elementx.className="contacts";
                    const elementy = document.createElement('a');
                    elementy.href = `/chat/${result.member}`;
                    elementy.innerHTML = `${result.member}`;
                    elementy.className='username';
                    elementx.append(elementy);
                    elementz = document.createElement('label');
                    elementz.innerHTML=`${result.status}`;
                    elementz.id="status";
                    elementx.append(elementz);
                document.querySelector('.contacts').after(elementx);
                
            }
            else if(result.message==='Username doesnot exist'){
                return false;
            }
          
          console.log(result);
      })
    };
}


document.body.addEventListener('click',function(event){
    if( event.srcElement.id === 'add' ){
        const element = event.srcElement
        const username= element.previousElementSibling.innerHTML;

fetch('/add', {
    method: 'POST',
    body: JSON.stringify({
        content: username,
        channel: document.querySelector('#room-name').innerHTML
    }),
    headers: { "X-CSRFToken": getCookie('csrftoken')}
  })
  .then(response => {
    if(response.status===201){
       lol = 1;
       return response.json();
    }
    else{
      lol = 2;
      return response.json();
    }
  })
  .then(result => {
        if(result.message==='member added'){
                const elementx = document.createElement('div');
                elementx.className="groups";
                const elementy = document.createElement('a');
                elementy.innerHTML = `${result.member}`;
                elementy.className='username';
                elementx.append(elementy);
                elementz = document.createElement('button');
                elementz.innerHTML="Remove From Group";
                elementz.className="btn btn-primary"
                elementz.id="remove";
                elementz.onclick
                elementx.append(elementz);
                elementm = document.createElement('button');
                elementm.innerHTML="Make admin";
                elementm.className="btn btn-primary"
                elementm.id="admin";
                elementx.append(elementm);
            document.querySelector('.groups').after(elementx);
            element.remove()
            
        }
        else if(result.message==='Username doesnot exist'){
            return false;
        }
      
      console.log(result);
  })
}
});

document.body.addEventListener('click',function(event){
    if( event.srcElement.id === 'remove' ){
        const element = event.srcElement
        const username= element.previousElementSibling.innerHTML;

fetch('/remove', {
    method: 'POST',
    body: JSON.stringify({
        content: username,
        channel: document.querySelector('#room-name').innerHTML
    }),
    headers: { "X-CSRFToken": getCookie('csrftoken')}
  })
  .then(response => {
    if(response.status===201){
       lol = 1;
       return response.json();
    }
    else{
      lol = 2;
      return response.json();
    }
  })
  .then(result => {
        if(result.message==='member added'){
                elementz = document.createElement('button');
                elementz.innerHTML="Add to Group";
                elementz.className="btn btn-primary"
                elementz.id="add";
            document.querySelectorAll('.contacts').forEach(elementl =>{
                if(elementl.firstElementChild.innerHTML===`${result.member}`){
                    elementl.firstElementChild.after(elementz)
                }
            })
            element.parentElement.remove()
            
        }
        else if(result.message==='Username doesnot exist'){
            return false;
        }
      
      console.log(result);
  })
}
}
)

document.body.addEventListener('click',function(event){
    if( event.srcElement.id === 'admin' ){
        const element = event.srcElement
        const username= element.previousElementSibling.previousElementSibling.innerHTML;

fetch('/admin', {
    method: 'POST',
    body: JSON.stringify({
        content: username,
        channel: document.querySelector('#room-name').innerHTML
    }),
    headers: { "X-CSRFToken": getCookie('csrftoken')}
  })
  .then(response => {
    if(response.status===201){
       lol = 1;
       return response.json();
    }
    else{
      lol = 2;
      return response.json();
    }
  })
  .then(result => {
        if(result.message===`you have given admin rights to ${username}`){
            element.previousElementSibling.remove()   
            element.remove()     
        }
        else if(result.message==='Username doesnot exist'){
            return false;
        }
      
      console.log(result);
  })
}
}
)

document.body.addEventListener('click',function(event){
    if( event.srcElement.id === 'removeadmin' ){
        const element = event.srcElement
        const username= element.previousElementSibling.innerHTML;

fetch('/radmin', {
    method: 'POST',
    body: JSON.stringify({
        content: username,
        channel: document.querySelector('#room-name').innerHTML
    }),
    headers: { "X-CSRFToken": getCookie('csrftoken')}
  })
  .then(response => {
    if(response.status===201){
       lol = 1;
       return response.json();
    }
    else{
      lol = 2;
      return response.json();
    }
  })
  .then(result => {
        if(result.message==='you have been removed from adminship'){
            window.history.back();  
        }
        else if(result.message==='Username doesnot exist'){
            return false;
        }
      
      console.log(result);
  })
}
}
)


document.querySelectorAll('.delete').forEach(element => {
    element.nextElementSibling.remove();
    element.remove();
    });
    document.querySelectorAll('.delete2').forEach(element => {
        element.nextElementSibling.nextElementSibling.remove()
        element.nextElementSibling.remove()
        element.remove()
        });


var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

const chatSocket2 = new WebSocket(
    ws_scheme+'://'
    + window.location.host
);

chatSocket2.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if(data.type==="chat_message"){
    const username = data.username
    document.querySelectorAll('.contacts').forEach(element =>{
        if(element.firstElementChild.innerHTML===username){
            if(element.firstElementChild.nextElementSibling===null){
            }
            else if(element.firstElementChild.nextElementSibling.id==='status'){
                element.firstElementChild.nextElementSibling.innerHTML=data.status
            }
        }
    })
}
else if(data.type==='notify'){
    if(data.message==='contact'){
        document.querySelectorAll('.contacts').forEach(element =>{
            if(element.firstElementChild.innerHTML===data.room){
                if(element.firstElementChild.nextElementSibling===null){

                }
                else{
                    element.querySelector('.unseen').innerHTML=(parseInt(element.querySelector('.unseen').innerHTML) || 0)+1
                }
            }
        })
    }
    if(data.message==='group'){
        document.querySelectorAll('.groups').forEach(element =>{
            if(element.firstElementChild.innerHTML===data.room){
                if(element.querySelector('.unseen2')===null){

                }
                else{
                    element.querySelector('.unseen2').innerHTML=(parseInt(element.querySelector('.unseen2').innerHTML) || 0)+1
                }
            }
        })
    }
}
else if(data.type==='xyz'){
    if(data.message==='contact'){
    const elementx = document.createElement('div');
                    elementx.className="contacts";
                    const elementy = document.createElement('a');
                    elementy.href = `/contact/${data.room}/`;
                    elementy.innerHTML = `${data.room}`;
                    elementy.className='username';
                    elementx.append(elementy);
                    elementz = document.createElement('label');
                    elementz.innerHTML='Online';
                    elementz.id="status";
                    elementx.append(elementz);
                    elementa = document.createElement('a');
                    elementa.className = "unseen"
                    elementx.append(elementa)
                document.querySelector('#hx2').after(elementx);
}
else if(data.message==='group'){
    const elementx = document.createElement('div');
                    elementx.className="groups";
                    const elementy = document.createElement('a');
                    elementy.href = `/contact/${data.room}/`;
                    elementy.innerHTML = `${data.room}`;
                    elementy.className='username';
                    elementx.append(elementy);
                    elementa = document.createElement('a');
                    elementa.className = "unseen2"
                    elementx.append(elementa)
                document.querySelector('#hx3').after(elementx);

}
else if(data.message==='remove'){
    document.querySelectorAll('.groups').forEach(element =>{
        if(element.firstElementChild.innerHTML===`${data.room}`){
            element.remove()
        }
    })
}
}
};

chatSocket2.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


if(document.querySelector('#room-name-input')!=null){
const chatSocketx = new WebSocket(
    ws_scheme+'://'
    + window.location.host
    +'/ws'
);

chatSocketx.onmessage = function(e) {
    const data = JSON.parse(e.data);
    for( k in data.noti){
        if(data.noti[k][1]=="contact"){
            document.querySelectorAll('.contacts').forEach(element =>{
                if(element.firstElementChild.innerHTML===`${k}`){
                    element.querySelector('.unseen').innerHTML=data.noti[k][0]
                }
            })
        }
        else{
            document.querySelectorAll('.groups').forEach(element =>{
                if(element.firstElementChild.innerHTML===`${k}`){
                    element.querySelector('.unseen2').innerHTML=data.noti[k][0]
                }
            })
        }
    }
    
};

chatSocketx.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

}



    // room page js
    if(document.querySelector('#chat-message-input')!=null){
const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const chatSocket = new WebSocket(
            ws_scheme+'://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if(data.type==='chat_message'){
            if(Array.isArray(data.message)){
                if(document.querySelector('#chat-log').value===""){
            data.message.forEach(element => {
                document.querySelector('#chat-log').value += (element + '\n');
            });
        }
        }
        else{
            document.querySelector('#chat-log').value += (data.message + '\n');
        }
        }
        else if(data.type==='add'){
            const elementx = document.createElement('div');
                elementx.className="contacts";
                const elementy = document.createElement('a');
                elementy.innerHTML = `${data.message}`;
                elementy.className = "username"
                elementx.append(elementy)
                document.querySelector('#hx3').after(elementx)
        }
        else if(data.type==='remove'){
            document.querySelectorAll('.contacts').forEach(element =>{
                if(element.firstElementChild.innerHTML===`${data.message}`){
                    element.remove()
                }
            })
        }
        else if(data.type==='addadmin'){
            const elementx = document.createElement('div');
            elementx.className="groups";
                const elementy = document.createElement('a');
                elementy.innerHTML = `${data.message}`;
                elementy.className = "username"
                elementx.append(elementy)
                document.querySelector('#hx2').after(elementx)
                document.querySelectorAll('.contacts').forEach(element =>{
                    if(element.firstElementChild.innerHTML===`${data.message}`){
                        element.remove()
                    }
                })
                const abc = document.querySelector('#usercx').innerHTML
                if(data.message===abc.substring(8,abc.length-9)){
                    const elementx = document.createElement('button');
                    elementx.className='btn btn-primary'
                    elementx.innerHTML='Settings'
                    elementx.id='settingxy'
                    document.querySelector('#goback').after(elementx)
                    document.body.addEventListener('click',function(event){
                        if( event.srcElement.id === 'settingxy' ){
                            window.location.href=window.location.href+"setting"
                        }
                    })
                }
        }
        else if(data.type==='radmin'){
            document.querySelectorAll('.groups').forEach(element =>{
                if(element.firstElementChild.innerHTML===`${data.message}`){
                    element.remove()
                }
            })
            const elementx = document.createElement('div');
                elementx.className="contacts";
                const elementy = document.createElement('a');
                elementy.innerHTML = `${data.message}`;
                elementy.className = "username"
                elementx.append(elementy)
                document.querySelector('#hx3').after(elementx)

        }
    }

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
        document.querySelector('#chat-message-input').focus();
        
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            if(document.querySelector('#hx2')===null){
                chatSocket.send(JSON.stringify({
                    'message': message,
                    'group':"contact"
                }));
            const abc = document.querySelector('#usercx').innerHTML
            abd = abc.substring(8,abc.length-9)
            chatSocket2.send(JSON.stringify({
                'status':"unknown",
                'roomname':abd,
                'message': "contact"
            }))
        }
        else{
            chatSocket.send(JSON.stringify({
                'message': message,
                'group':"group"
            }));
            chatSocket2.send(JSON.stringify({
                'status':"unknown",
                'roomname':document.querySelector('#heading').innerHTML,
                'message': "group"
            }))
        }
            messageInputDom.value = '';
        };
    }




if(document.querySelector('.container')!=null){
if(document.querySelector('.container').firstElementChild.id==='note'){
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    
            const chatSocket3 = new WebSocket(
                ws_scheme+'://'
                + window.location.host
                + '/ws/chat/'
                + roomName
                + '/'
                + 'setting'

            );
    
            chatSocket3.onmessage = function(e) {
                const data = JSON.parse(e.data);
                if(data.message==='add'){
                    const elementx = document.createElement('div');
                elementx.className="groups";
                const elementy = document.createElement('a');
                elementy.innerHTML = `${data.username}`;
                elementy.className='username';
                elementx.append(elementy);
                elementz = document.createElement('button');
                elementz.innerHTML="Remove From Group";
                elementz.className="btn btn-primary"
                elementz.id="remove";
                elementx.append(elementz);
                elementm = document.createElement('button');
                elementm.innerHTML="Make admin";
                elementm.className="btn btn-primary"
                elementm.id="admin";
                elementx.append(elementm);
            document.querySelector('.groups').after(elementx);
            document.querySelectorAll('.contacts').forEach(element =>{
                if(element.firstElementChild.innerHTML===data.username){
                    element.firstElementChild.nextElementSibling.remove()
                }
            })
                }

                else if(data.message==='remove'){
                    elementz = document.createElement('button');
                elementz.innerHTML="Add to Group";
                elementz.className="btn btn-primary"
                elementz.id="add";
            document.querySelectorAll('.contacts').forEach(elementl =>{
                if(elementl.firstElementChild.innerHTML===`${data.username}`){
                    elementl.firstElementChild.after(elementz)
                }
            })
           document.querySelectorAll('.groups').forEach(element =>{
            if(element.firstElementChild.innerHTML===data.username){
                element.remove()
            }
           })
            
        }
        else if(data.message==='add admin'){
            document.querySelectorAll('.groups').forEach(element =>{
                if(element.firstElementChild.innerHTML===data.username){
                    element.firstElementChild.nextElementSibling.nextElementSibling.remove()
                    element.firstElementChild.nextElementSibling.remove()
                }
               })
        }
        else if(data.message==='remove admin'){
            document.querySelectorAll('.groups').forEach(element =>{
            if(element.firstElementChild.innerHTML===data.username){
                elementz = document.createElement('button');
                elementz.innerHTML="Remove From Group";
                elementz.className="btn btn-primary"
                elementz.id="remove";
                element.append(elementz)
                elementm = document.createElement('button');
                elementm.innerHTML="Make admin";
                elementm.className="btn btn-primary"
                elementm.id="admin";
                element.append(elementm)
                }
               })

        }

                }
            

    
            chatSocket3.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };
            
        }

    }  
        
    });
