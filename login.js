const loginForm = document.getElementById("loginForm");
const errorMessage = document.getElementById("errorMessage");

// Hardcoded credentials for demonstration purposes
const VALID_USERNAME = "admin";
const VALID_PASSWORD = "password";

loginForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent form submission

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    // Validate credentials
    if (username === VALID_USERNAME && password === VALID_PASSWORD) {
        // Redirect to homepage
        localStorage.setItem("isLoggedIn", "true");

        window.location.href = "index.html";
    } else {
        // Show error message
        errorMessage.style.display = "block";
    }
});

