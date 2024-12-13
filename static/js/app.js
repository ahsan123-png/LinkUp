// WebSocket instance
let currentSocket = null;

// DOM Elements
const attachmentBtn = document.getElementById('attachment-btn');
const attachmentPopup = document.getElementById('attachment-popup');
const overlay = document.getElementById('overlay');
const sendBtn = document.getElementById('send-btn');
const chatContent = document.querySelector('.chat-content');
const inputField = document.querySelector('input[type="text"]');

// Toggle attachment popup
attachmentBtn.addEventListener('click', () => {
    attachmentPopup.classList.toggle('hidden');
    overlay.classList.toggle('hidden');
});

overlay.addEventListener('click', () => {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
});

// Handle attachment options
function closePopup() {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
}

document.getElementById('photos-videos').addEventListener('click', () => {
    alert('Select Photos & Videos');
    closePopup();
});

document.getElementById('camera').addEventListener('click', () => {
    alert('Open Camera');
    closePopup();
});

document.getElementById('document').addEventListener('click', () => {
    alert('Select Documents');
    closePopup();
});

// Handle sending messages
sendBtn.addEventListener('click', () => {
    const message = inputField.value.trim();
    if (message) {
        // Send message through WebSocket
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: message }));
        }

        // Display sent message locally
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'sent');
        messageElement.innerHTML = `<p>${message}</p><span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>`;
        chatContent.appendChild(messageElement);
        inputField.value = '';
        chatContent.scrollTop = chatContent.scrollHeight;
    }
});

// jQuery to handle chat switching
$(document).ready(function () {
    $(".chat-item").click(function () {
        const selectedUser = $(this).data("user");

        // Update active chat UI
        $(".chat-item").removeClass("active");
        $(this).addClass("active");
        $("#chat-header-user").text(selectedUser);
        $(".chat-messages").addClass("hidden");
        $(`.chat-messages[data-user='${selectedUser}']`).removeClass("hidden");

        // Close existing WebSocket connection
        if (currentSocket) {
            currentSocket.close();
        }

        // Establish new WebSocket connection for the selected user
        const socketUrl = `ws://127.0.0.1:8000/ws/chat/${selectedUser}/`;
        currentSocket = new WebSocket(socketUrl);

        currentSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const { message, sender } = data;

            // Append received message to the chat
            const messageHTML = `
                <div class="message received">
                    <p>${message}</p>
                    <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
            `;
            $(`.chat-messages[data-user='${sender}']`).append(messageHTML);
        };

        currentSocket.onerror = function (error) {
            console.error("WebSocket Error:", error);
        };

        currentSocket.onclose = function () {
            console.warn("WebSocket closed for user:", selectedUser);
        };
    });

    $("#send-btn").click(function () {
        const messageInput = $("#message-input").val().trim();
        const currentUser = $("#chat-header-user").text();

        if (messageInput === "") {
            alert("Please type a message!");
            return;
        }

        // Send message to WebSocket
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: messageInput }));
        }

        // Display sent message in the chat
        const messageHTML = `
            <div class="message sent">
                <p>${messageInput}</p>
                <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
        `;
        $(`.chat-messages[data-user='${currentUser}']`).append(messageHTML);
        $("#message-input").val("");
    });
});
