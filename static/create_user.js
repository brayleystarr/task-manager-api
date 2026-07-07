document.getElementById("register-btn").addEventListener("click", async () => {
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="password"]').value;

  try {
    const response = await fetch("/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Registration failed");
      return;
    }

    // success — redirect to login
    window.location.href = "/register";
  } catch (err) {
    alert("Something went wrong. Please try again.");
  }
});

document.getElementById("login-btn").addEventListener("click", async () => {
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="password"]').value;

  try {
    const response = await fetch("/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Login failed");
      return;
    }

    window.location.href = "/testing";
  } catch (err) {
    alert("Something went wrong. Please try again.");
  }
});