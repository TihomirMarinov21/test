const socket = new WebSocket(
    "wss://test-messenger-tl.onrender.com"
);

const user = prompt("What is your name ?")

const messages =
    document.getElementById("messages");

socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    addMessage(
        data.username + ": " + data.message
    );

};

function addMessage(text) {

    const div =
        document.createElement("div");

    div.className = "message";
    div.innerText = text;

    messages.appendChild(div);
}

function sendMessage() {

    const input = document.getElementById("messageInput");
    if (input.value.trim() != ""){
        socket.send(
            JSON.stringify(
                {
                    username: user,
                    message: input.value
                }
            )
            addMessage( user + ": " + input.value);
        );
    };


    input.value = "";
}

socket.onopen = () => {
    console.log("CONNECTED TO RENDER");
};

socket.onerror = (e) => {
    console.log("ERROR");
    console.log(e);
};

document.getElementById("messageInput")
.addEventListener("keydown", (event) => {
    if(event.key === "Enter"){
        sendMessage();
    }
});
