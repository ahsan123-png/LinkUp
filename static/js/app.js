// WebSocket instance
let currentSocket = null;

// DOM Elements
const attachmentBtn = document.getElementById('attachment-btn');
const attachmentPopup = document.getElementById('attachment-popup');
const overlay = document.getElementById('overlay');
const sendBtn = document.getElementById('send-btn');
const chatContent = document.querySelector('.chat-content');
const inputField = document.querySelector('input[type="text"]');

// Base API URL
const apiUrl = "http://127.0.0.1:8000/users/api/chat"; // Update with your backend's URL

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
    // Replace with actual photo/video selection functionality
    closePopup();
});

document.getElementById('camera').addEventListener('click', () => {
    // Replace with camera functionality
    closePopup();
});

document.getElementById('document').addEventListener('click', () => {
    // Replace with document selection functionality
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

        // Fetch chat history for the selected user
        fetchChatHistory(selectedUser);

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

            // Append received message to the chat content
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', 'received');
            messageElement.innerHTML = `
                <p>${message}</p>
                <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            `;
            chatContent.appendChild(messageElement);
            chatContent.scrollTop = chatContent.scrollHeight; // Scroll to the latest message
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
            return; // Don't send empty messages
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
        chatContent.append(messageHTML);
        $("#message-input").val(""); // Clear the input field
        chatContent.scrollTop = chatContent.scrollHeight; // Scroll to latest message
    });
});
