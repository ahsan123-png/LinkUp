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
window.onload = function () {
    const modal = document.getElementById("search-modal"); 
    modal.style.display = "none"; 
};
const searchBtn = document.getElementById("search-btn");
const searchModal = document.getElementById("search-modal");
const closeModalBtn = document.getElementById("close-modal");
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");

searchBtn.addEventListener("click", function () {
    searchModal.style.display = "flex"; // Show modal
});
closeModalBtn.addEventListener("click", function () {
    searchModal.style.display = "none"; // Hide modal
});
window.addEventListener("click", function (event) {
    if (event.target === searchModal) {
        searchModal.style.display = "none";
    }
});
const users = ["John Doe", "Jane Smith", "Emily Johnson", "Michael Brown", "Sarah Wilson"];
searchInput.addEventListener("input", function () {
    const query = searchInput.value.toLowerCase();
    searchResults.innerHTML = ""; // Clear previous results
    users.forEach((user) => {
        if (user.toLowerCase().includes(query)) {
            const resultItem = document.createElement("p");
            resultItem.textContent = user;
            resultItem.addEventListener("click", function () {
                alert(`You selected: ${user}`); // Action for selecting a user
                searchModal.style.display = "none"; // Close modal after selecting a user
            });
            searchResults.appendChild(resultItem);
        }
    });
    if (!searchResults.innerHTML) {
        searchResults.innerHTML = "<p>No results found</p>"; // Display message when no results found
    }
});