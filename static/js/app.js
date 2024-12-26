// WebSocket instance
let currentSocket = null;

// DOM Elements
const attachmentBtn = document.getElementById('attachment-btn');
const attachmentPopup = document.getElementById('attachment-popup');
const overlay = document.getElementById('overlay');
const sendBtn = document.getElementById('send-btn');
const chatContent = document.querySelector('.chat-content');
const inputField = document.querySelector('input[type="text"]');
const apiUrl = "http://127.0.0.1:8000/users/api/chat"; // Update with your backend's URL
attachmentBtn.addEventListener('click', () => {
    attachmentPopup.classList.toggle('hidden');
    overlay.classList.toggle('hidden');
});
overlay.addEventListener('click', () => {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
});
async function fetchChatHistory(selectedUser) {
    try {
        const response = await fetch(`${apiUrl}/history/${selectedUser}/`);
        const chatHistory = await response.json();
        chatContent.innerHTML = "";
        chatHistory.forEach(message => {
            appendMessage(message.content, message.sender === selectedUser ? 'received' : 'sent', new Date(message.sent_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        });
        chatContent.scrollTop = chatContent.scrollHeight;
    } catch (error) {
        console.error("Error fetching chat history:", error);
    }
}
function appendMessage(content, className, time) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    messageElement.innerHTML = `<p>${content}</p><span class="message-time">${time}</span>`;
    chatContent.appendChild(messageElement);
}
sendBtn.addEventListener('click', () => {
    const message = inputField.value.trim();
    if (message) {
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: message }));
        }
        inputField.value = '';
    }
});
$(document).ready(function () {
    $(".chat-item").click(function () {
        const selectedUser = $(this).data("user");
        $(".chat-item").removeClass("active");
        $(this).addClass("active");
        $("#chat-header-user").text(selectedUser);
        fetchChatHistory(selectedUser);
        if (currentSocket) {
            currentSocket.close();
        }
        const socketUrl = `ws://127.0.0.1:8000/ws/chat/${selectedUser}/`;
        currentSocket = new WebSocket(socketUrl);
        currentSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const { message, sender } = data;
            appendMessage(message, sender === selectedUser ? 'received' : 'sent', new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
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
            return; 
        }
        if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
            currentSocket.send(JSON.stringify({ message: messageInput }));
        }
        inputField.val(''); 
        chatContent.scrollTop = chatContent.scrollHeight; 
    });
});
