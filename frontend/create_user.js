// Select the form element by its ID
document.getElementById("createUserForm")
    // Listen for when the form is submitted
    .addEventListener("submit", async function (e) {

    // Prevent default form behavior (page reload)
    e.preventDefault();

    // Get the value entered in the username input
    const username = document.getElementById("username").value;

    // Get the value entered in the password input
    const password = document.getElementById("password").value;

    // Send data to FastAPI backend using HTTP POST request
    const response = await fetch("http://127.0.0.1:8000/users", {
        method: "POST", // HTTP method type

        headers: {
            "Content-Type": "application/json"
            // Tells backend we are sending JSON data
        },

        body: JSON.stringify({
            username: username,
            password: password
            // Convert JS object into JSON string for backend
        })
    });

    // Select the message element on the page
    const messageEl = document.getElementById("message");

    // Check if request was successful (status 200–299)
    if (response.ok) {

        // Convert response JSON into JS object
        const data = await response.json();

        // Show success message on page
        messageEl.innerText = "User created successfully!";

        // Print backend response in browser console (debugging)
        console.log(data);

    } else {
        // If backend returned error status
        messageEl.innerText = "Error creating user";
    }
});