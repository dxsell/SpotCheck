// Check if the user is logged in

// Initialize the map
const map = L.map('map').setView([51.505, -0.09], 2);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add the search control
L.Control.geocoder().addTo(map);

// Flag to track form visibility
let formVisible = false;

// Reverse Geocoding
const geocoder = L.Control.Geocoder.nominatim();

map.on('click', function (e) {
    const { lat, lng } = e.latlng;

    geocoder.reverse(e.latlng, map.options.crs.scale(map.getZoom()), results => {
        if (results.length > 0) {
            const address = results[0].name;
            document.getElementById('address').innerText = address; // Update the address field
        }
        if (formVisible) {
            form.classList.remove('show');
            formVisible = false;
        } else {
            document.getElementById('lat').value = lat;
            document.getElementById('lng').value = lng;
            form.style.display = 'block';
            form.classList.add('show');
            formVisible = true;
        }
    });
});

// Handle map click event
const form = document.getElementById('reviewForm');
form.classList.add('hidden');
map.on('click', function (e) {
    const { lat, lng } = e.latlng;

});

//Star Highlighting
document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('click', function () {
        const value = this.dataset.value;
        document.querySelectorAll('.star').forEach(s => {
            s.classList.remove('selected');
            if (s.dataset.value <= value) {
                s.classList.add('selected');
            }
        });
        this.classList.add('selected');
        document.getElementById('rating').dataset.rating = value; // Store rating value
    });
});

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

document.getElementById('form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const lat = document.getElementById('lat').value;
    const lng = document.getElementById('lng').value;
    const review = document.getElementById('review').value;
    const rating = document.getElementById('rating').dataset.rating || "0"; // Default rating
    const address = document.getElementById('address').innerText;

    // Add marker to the map
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`${address}<br><b>Review:</b><br>${review}<br><b>Rating:</b> ${rating} stars`).openPopup();

    // Save Marker
    const userMarkers = JSON.parse(localStorage.getItem("userMarkers") || "[]");
    userMarkers.push({ lat, lng, address, review, rating });
    localStorage.setItem("userMarkers", JSON.stringify(userMarkers));

    // Show confirmation message
    document.getElementById('confirmation').style.display = 'block';
    setTimeout(() => {
        document.getElementById('confirmation').style.display = 'none';
    }, 3000);

    // Hide the form
    const form = document.getElementById('reviewForm');
    form.style.display = 'none';
    formVisible = false;
    document.getElementById('form').reset();
});