async function sendMessage(){

    const input = document.getElementById("user-input");

    const message = input.value;

    if(message==="")
        return;

    const chatBox=document.getElementById("chat-box");

    chatBox.innerHTML += `
    <div class="user-message">
    ${message}
    </div>
   `;

    const response=await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            message:message

        })

    });

    const data=await response.json();

    chatBox.innerHTML += `
    <div class="bot-message">
    ${data.response}
    </div>
    `;
    input.value="";

    chatBox.scrollTop=chatBox.scrollHeight;
}

document
.getElementById("user-input")
.addEventListener("keypress",function(event){

    if(event.key==="Enter"){

        sendMessage();

    }

});

document.getElementById("user-input").focus();

window.onload=function(){

document.getElementById("chat-box").innerHTML=`

<div class="bot-message">
Welcome to the AI Registration Assistant!

I can help you:

• Register as a student
• Guide you through the registration process
• Answer basic registration-related questions

Type "register" to begin.

</div>

`;

}