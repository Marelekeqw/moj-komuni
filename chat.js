let ws;
let username;

function login() {
    username = document.getElementById("username").value.trim();
    if (!username) {
        alert("Podaj nazwę użytkownika");
        return;
    }

    document.getElementById("login-box").style.display = "none";
    document.getElementById("chat-box").style.display = "block";

    ws = new WebSocket(`ws://127.0.0.1:8000/ws/${username}`);
    ws.onmessage = function(event) {
        const messages = document.getElementById("messages");

        // Tworzymy nowy element wiadomości
        const msgDiv = document.createElement("div");
        msgDiv.textContent = event.data;

        // Dodajemy go do kontenera
        messages.appendChild(msgDiv);

        // Scroll na dół
        messages.scrollTop = messages.scrollHeight;
    };
}

function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const fileInput = document.getElementById("fileInput");

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = () => {
            ws.send(JSON.stringify({file: file.name, data: reader.result}));
        };
        reader.readAsDataURL(file);
        fileInput.value = "";
    } else if (messageInput.value.trim() !== "") {
        ws.send(JSON.stringify({message: messageInput.value}));
        messageInput.value = "";
    }
}
