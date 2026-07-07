
const socket = new WebSocket(
    "wss://test-messenger-tl.onrender.com"
);

const user = prompt("What is your name?") || "Anonymous";

const messages =
    document.getElementById("messages");

socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    if (data.type === "image") {

        const img =
            document.createElement("img");

        img.src = data.data;
        img.style.maxWidth = "250px";
        img.style.display = "block";
        img.style.margin = "5px";

        messages.appendChild(img);

        messages.scrollTop =
            messages.scrollHeight;

    } else {

        addMessage(
            data.username + ": " + data.message
        );

    }
};

function addMessage(text) {

    const div =
        document.createElement("div");

    const now =
        new Date();

    const time =
        now.getHours().toString().padStart(2, "0")
        + ":" +
        now.getMinutes().toString().padStart(2, "0");

    div.className = "message";
    div.innerText =
        text + " [" + time + "]";

    messages.appendChild(div);

    messages.scrollTop =
        messages.scrollHeight;
}

function sendMessage() {

    const input =
        document.getElementById("messageInput");

    if (input.value.trim() === "") {
        return;
    }

    socket.send(
        JSON.stringify({
            type: "text",
            username: user,
            message: input.value
        })
    );

    input.value = "";
}

function sendImage() {

    const file =
        document.getElementById("imageInput")
        .files[0];

    if (!file) {
        return;
    }

    const reader =
        new FileReader();

    reader.onload = () => {

        socket.send(
            JSON.stringify({
                type: "image",
                username: user,
                data: reader.result
            })
        );
    };

    reader.readAsDataURL(file);
}

socket.onopen = () => {
    console.log("CONNECTED TO RENDER");
};

socket.onerror = (e) => {
    console.log("ERROR");
    console.log(e);
};

document
    .getElementById("messageInput")
    .addEventListener("keydown", (event) => {

        if (event.key === "Enter") {
            sendMessage();
        }

    });
