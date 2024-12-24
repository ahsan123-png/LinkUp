let currentSocket = null;
const attachmentBtn = document.getElementById('attachment-btn');
const attachmentPopup = document.getElementById('attachment-popup');
const overlay = document.getElementById('overlay');
const sendBtn = document.getElementById('send-btn');
const chatContent = document.querySelector('.chat-content');
const inputField = document.querySelector('input[type="text"]');
attachmentBtn.addEventListener('click', () => {
    attachmentPopup.classList.toggle('hidden');
    overlay.classList.toggle('hidden');
});
overlay.addEventListener('click', () => {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
});

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

// Fetch chat history from the server
async function fetchChatHistory(selectedUser) {
    try {
        const response = await fetch(`${apiUrl}/history/${selectedUser}/`);
        const chatHistory = await response.json();

        // Clear existing chat messages
        chatContent.innerHTML = "";

        // Append messages to chat content
        chatHistory.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', message.sender === selectedUser ? 'received' : 'sent');
            messageElement.innerHTML = `
                <p>${message.content}</p>
                <span class="message-time">${new Date(message.sent_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            `;
            chatContent.appendChild(messageElement);
        });

        chatContent.scrollTop = chatContent.scrollHeight;
    } catch (error) {
        console.error("Error fetching chat history:", error);
    }
}
sendBtn.addEventListener('click', () => {
    const message = inputField.value.trim();
    if (message) {
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: message }));
        }
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'sent');
        messageElement.innerHTML = `<p>${message}</p><span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>`;
        chatContent.appendChild(messageElement);
        inputField.value = '';
        chatContent.scrollTop = chatContent.scrollHeight;
    }
});
$(document).ready(function () {
    $(".chat-item").click(function () {
        const selectedUser = $(this).data("user");
        $(".chat-item").removeClass("active");
        $(this).addClass("active");
        $("#chat-header-user").text(selectedUser);
        $(".chat-messages").addClass("hidden");
        $(`.chat-messages[data-user='${selectedUser}']`).removeClass("hidden");
        if (currentSocket) {
            currentSocket.close();
        }
        const socketUrl = `ws://127.0.0.1:8000/ws/chat/${selectedUser}/`;
        currentSocket = new WebSocket(socketUrl);
        currentSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const { message, sender } = data;
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
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: messageInput }));
        }
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
