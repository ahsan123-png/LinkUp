document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('signup-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const dob = document.getElementById('dob').value;
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirm-password').value.trim();

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Validate Date of Birth (ensure it's not in the future)
        const today = new Date().toISOString().split('T')[0]; // Current date in YYYY-MM-DD format
        if (dob >= today) {
            alert("Please select a valid date of birth.");
            return;
        }

        // Submit the form data (for real application, you will need to send this to your server)
        console.log('Username:', username);
        console.log('Email:', email);
        console.log('Date of Birth:', dob);
        console.log('Password:', password);

        alert("Sign-Up Successful! You can now log in.");
        // Redirect to login page
        window.location.href = "login.html";
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
        
            // Submit the form data (for real application, you will need to send this to your server)
            console.log('Email:', email);
            console.log('Password:', password);
        
            alert("Login Successful!");
            // Redirect to the chat page after login
            window.location.href = "index.html";
        });
            console.log('Login form submitted');
    } else {
        console.error('Login form not found');
    }
});

