


if (isLoggedIn === "true") {
    // Get the navigation bar
    const navBar = document.querySelector(".nav");

    // Create the "My Account" button
    const myAccountButton = document.createElement("a");
    myAccountButton.href = "/accountsPage.html"; // Adjust the href as needed
    myAccountButton.textContent = "My Account";
    myAccountButton.style.float = "right"; // Align to the right
    myAccountButton.style.marginRight = "10px";

    // Create the "Logout" button
    const logoutButton = document.createElement("a");
    logoutButton.href = "#"; // Use "#" or leave href empty to prevent navigation
    logoutButton.textContent = "Logout";
    logoutButton.style.float = "right";
    logoutButton.style.marginRight = "10px";

    // Append buttons to the navigation bar
    navBar.appendChild(logoutButton);
    navBar.appendChild(myAccountButton);
    navBar.removeChild(loginButton);

    // Add logout functionality
    logoutButton.addEventListener("click", () => {
        // Clear login state
        localStorage.removeItem("isLoggedIn");

        // Redirect to the login page
        window.location.href = "LoginPage.html";
    });
}