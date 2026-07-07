const socket = new WebSocket(
    "wss://test-messenger-tl.onrender.com"
);

const messages =
    document.getElementById("messages");

socket.onmessage = (event) => {

    addMessage(event.data);
};

function addMessage(text) {

    const div =
        document.createElement("div");

    div.className = "message";
    div.innerText = text;

    messages.appendChild(div);
}

function sendMessage() {

    const input =
        document.getElementById(
            "messageInput"
        );

    socket.send(input.value);

    addMessage("Me: " + input.value);

    input.value = "";
}
