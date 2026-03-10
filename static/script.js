async function sendMessage(){

let msg = document.getElementById("message").value;

if(msg.trim() === "") return;

let chat = document.getElementById("chatbox");

// show user message
chat.innerHTML += "<p><b>You:</b> " + msg + "</p>";

try{

let res = await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({message:msg})
});

let data = await res.json();

// show bot response
chat.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";

}catch(error){

chat.innerHTML += "<p><b>Error:</b> Server not responding</p>";

}

// clear input
document.getElementById("message").value = "";

// auto scroll
chat.scrollTop = chat.scrollHeight;

}