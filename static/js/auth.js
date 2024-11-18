document.addEventListener('DOMContentLoaded', function () {
    const homeUrl = document.getElementById('home-url').getAttribute('data-home-url');
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Collect form data
            const fullName = document.getElementById('full-name').value.trim();
            const phoneNumber = document.getElementById('phone-number').value.trim();
            const email = document.getElementById('email').value.trim();
            const dob = document.getElementById('dob').value;
            const password = document.getElementById('password').value.trim();
            const confirmPassword = document.getElementById('confirm-password').value.trim();

            // Password validation
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

            // Data to send in the AJAX request
            const data = {
                full_name: fullName,
                email: email,
                phone_number: phoneNumber,
                password: password
            };

            // Use jQuery AJAX to send the POST request
            $.ajax({
                url: 'http://127.0.0.1:8000/users/register/',  // API endpoint
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),  // Convert data to JSON string
                success: function(response) {
                    // On success, handle response and redirect
                    alert("Sign-Up Successful! You can now log in.");
                    window.location.href = homeUrl;  // Redirect to the homepage
                },
                error: function(xhr, status, error) {
                    // On error, handle it
                    let errorMessage = "An error occurred. Please try again.";
                    if (xhr.responseJSON && xhr.responseJSON.errors) {
                        errorMessage = JSON.stringify(xhr.responseJSON.errors);
                    }
                    alert("Error: " + errorMessage);
                }
            });
        });
    }
});

//     // Handle login form submission
//     const loginForm = document.getElementById('login-form');
//     if (loginForm) {
//         loginForm.addEventListener('submit', function (e) {
//             e.preventDefault();
//             // Get the identifier (can be email or phone number) and password values
//             const identifier = document.getElementById('identifier').value.trim();
//             const password = document.getElementById('password').value.trim();
//             const data = {
//                 username: identifier,  // 'username' is either the email or phone number
//                 password: password
//             };
//             fetch('/users/login/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify(data)
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.error) {
//                     // Handle errors from the API
//                     alert("Error: " + data.error);
//                 } else {
//                     // If login is successful, store JWT token and redirect
//                     localStorage.setItem('access_token', data.access_token);  // Store JWT token
//                     localStorage.setItem('refresh_token', data.refresh_token);  // Store refresh token

//                     alert("Login Successful!");
//                     window.location.href = homeUrl;  // Redirect to home page
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 alert("An error occurred. Please try again.");
//             });
//         });
//     } else {
//         console.error('Login form not found');
//     }
// });