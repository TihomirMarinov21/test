
const socket = new WebSocket(
    "wss://test-messenger-tl.onrender.com"
); // create a websocket

const user = prompt("What is your name?") || "Anonymous"; // ask for the user's name if none given Anonymous by default

const messages =
    document.getElementById("messages"); // access the message container

/*
after receiving data we check if its an image if it is not we asume it is text.
We have function for each case image and regular text message.
*/
socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    if (data.type === "image") {

        const img =
            document.createElement("img"); // create an image html component

        // give the necessary attributes
        img.src = data.data;
        img.style.maxWidth = "250px";
        img.style.display = "block";
        img.style.margin = "5px";

        messages.appendChild(img); // add in the chat

        messages.scrollTop =
            messages.scrollHeight; // make sure the container always scrolls down to the newest message

    } else {

        addMessage(
            data.username + ": " + data.message // if not an image return who sent what
        );

    }
};

function addMessage(text) {

    const div =
        document.createElement("div"); // create the component holding the content of the message

    const now =
        new Date(); // creating a date object that has all the current time and date

    const time = // filter since we only want to see the hour and minute the message was sent, also making it always 2 digits
        now.getHours().toString().padStart(2, "0")
        + ":" +
        now.getMinutes().toString().padStart(2, "0");

    div.className = "message"; // assign a class to the div to addapt the necessary css properties
    div.innerText =
        text + " [" + time + "]"; // add time to the text

    messages.appendChild(div); // adds the div to the message container

    messages.scrollTop =
        messages.scrollHeight; // chat always scrollt down to the newest message
}

function sendMessage() {

    const input =
        document.getElementById("messageInput"); // take what the user submits in the input field

    if (input.value.trim() === "") { // prevent empty messages, if empty quick exit of this function
        return;
    }

    socket.send( // send the message as a json structure
        JSON.stringify({
            type: "text",
            username: user,
            message: input.value
        })
    );

    input.value = ""; // empty the input for better user experience
}

function sendImage() {

    const file =
        document.getElementById("imageInput")
        .files[0]; // files contains all selected files, we take the first one

    if (!file) {
        return;
    } // exit if no image was selected
    
    const reader =
        new FileReader(); // FileReader converts the selected file into a string that can be sent through the WebSocket
    reader.onload = () => {

        socket.send( // convert the JavaScript object into a string so it can be sent through the WebSocket
            JSON.stringify({
                type: "image",
                username: user,
                data: reader.result
            })
        );
    };

    reader.readAsDataURL(file);
}

socket.onopen = () => { // log successful connection to the Render server
    console.log("CONNECTED TO RENDER");
};

socket.onerror = (e) => { // in case of an error occuring we will be notified in the dev tools of the browser
    console.log("ERROR");
    console.log(e);
};

document
    .getElementById("messageInput") // selecting the input fields and giving them the ability to listen when a user presses ENTER 
    // to trigger the send message functionality
    .addEventListener("keydown", (event) => { // 

        if (event.key === "Enter") {
            sendMessage();
        }

    });
