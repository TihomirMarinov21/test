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
    if (input.value !="") {
        socket.send(input.value)
    };

    addMessage("Me: " + input.value);

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
