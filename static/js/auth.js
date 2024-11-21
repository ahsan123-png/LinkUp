document.addEventListener('DOMContentLoaded', function () {
    const homeUrl = document.getElementById('home-url').getAttribute('data-home-url');

    // Handle Signup Form Submission
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

            // Validate inputs
            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            const today = new Date().toISOString().split('T')[0];
            if (dob >= today) {
                alert("Please select a valid date of birth.");
                return;
            }

            // Prepare data for API
            const data = {
                full_name: fullName,
                email: email,
                phone_number: phoneNumber,
                password: password,
                dob: dob
            };

            console.log("Sending data to backend:", data); // Debugging

            // Send POST request to backend
            fetch('http://127.0.0.1:8000/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                console.log("Response status:", response.status); // Debugging
                if (!response.ok) {
                    return response.json().then(err => {
                        console.error("Error response from backend:", err); // Debugging
                        throw err;
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Success response from backend:", data); // Debugging
                alert("Sign-Up Successful! You can now log in.");
                window.location.href = homeUrl;
            })
            .catch(error => {
                console.error("Error during fetch:", error); // Debugging
                let errorMessage = "An error occurred. Please try again.";
                if (error.errors) {
                    errorMessage = JSON.stringify(error.errors);
                }
                alert("Error: " + errorMessage);
            });
        });
    }
});


    // Handle Login Form Submission
    // const loginForm = document.getElementById('login-form');
    // if (loginForm) {
    //     loginForm.addEventListener('submit', function (e) {
    //         e.preventDefault();

    //         // Get identifier and password
    //         const identifier = document.getElementById('identifier').value.trim();
    //         const password = document.getElementById('password').value.trim();

    //         // Prepare data for API
    //         const data = {
    //             username: identifier, // Assuming "username" can be email or phone
    //             password: password,
    //         };

    //         // Send POST request to backend
    //         fetch('http://127.0.0.1:8000/users/login/', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify(data),
    //         })
    //         .then(response => {
    //             if (!response.ok) {
    //                 return response.json().then(err => {
    //                     throw err;
    //                 });
    //             }
    //             return response.json();
    //         })
    //         .then(data => {
    //             localStorage.setItem('access_token', data.access_token);
    //             localStorage.setItem('refresh_token', data.refresh_token);

    //             alert("Login Successful!");
    //             window.location.href = homeUrl;
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert("An error occurred. Please try again.");
    //         });
    //     });
    // } else {
    //     console.error('Login form not found');
    // }
// });
