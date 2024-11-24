const attachmentBtn = document.getElementById('attachment-btn');
const attachmentPopup = document.getElementById('attachment-popup');
const overlay = document.getElementById('overlay');
const sendBtn = document.getElementById('send-btn');
const chatContent = document.querySelector('.chat-content');
const inputField = document.querySelector('input[type="text"]');

// Open/Close Attachment Popup
attachmentBtn.addEventListener('click', () => {
    attachmentPopup.classList.toggle('hidden');
    overlay.classList.toggle('hidden');
});

// Close popup when clicking outside
overlay.addEventListener('click', () => {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
});

// Simulate file selection for attachment options
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

function closePopup() {
    attachmentPopup.classList.add('hidden');
    overlay.classList.add('hidden');
}

// Send message
sendBtn.addEventListener('click', () => {
    const message = inputField.value.trim();
    if (message) {
        // Append sent message to chat content
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'sent');
        messageElement.innerHTML = `<p>${message}</p><span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>`;
        chatContent.appendChild(messageElement);
        
        // Clear input field
        inputField.value = '';

        // Scroll chat to the bottom
        chatContent.scrollTop = chatContent.scrollHeight;
    }
});
$(document).ready(function () {
    // Handle chat switching
    $(".chat-item").click(function () {
        const selectedUser = $(this).data("user");

        // Highlight the selected chat item
        $(".chat-item").removeClass("active");
        $(this).addClass("active");

        // Update the chat header
        $("#chat-header-user").text(selectedUser);

        // Show the selected chat messages and hide others
        $(".chat-messages").addClass("hidden");
        $(`.chat-messages[data-user='${selectedUser}']`).removeClass("hidden");
    });

    // Handle sending a message
    $("#send-btn").click(function () {
        const messageInput = $("#message-input").val().trim();
        const currentUser = $("#chat-header-user").text();

        if (messageInput === "") {
            alert("Please type a message!");
            return;
        }
        // Create and append the sent message
        const messageHTML = `
            <div class="message sent">
                <p>${messageInput}</p>
                <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
        `;
        $(`.chat-messages[data-user='${currentUser}']`).append(messageHTML);
        // Clear the input field
        $("#message-input").val("");
    });
});
