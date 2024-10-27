const fileInput = document.getElementById('file-input');
const profileImg = document.getElementById('profile-img');
const userStatus = document.getElementById('user-status');
const statusInput = document.getElementById('status-input');
const userName = document.getElementById('user-name');
const nameInput = document.getElementById('name-input');

// Update Profile Image
fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            profileImg.src = event.target.result;
        }
        reader.readAsDataURL(file);
    }
});

// Update Status
document.getElementById('update-status').addEventListener('click', function() {
    userStatus.textContent = statusInput.value || 'Available';
    statusInput.value = '';
});

// Update Name
document.getElementById('update-name').addEventListener('click', function() {
    userName.textContent = nameInput.value || 'User Name';
    nameInput.value = '';
});