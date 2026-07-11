document.getElementById("login-btn").addEventListener("click", async () => {
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="password"]').value;

  // check for existing token
  
  const token = localStorage.getItem("token")
  if (token) {
      const response = await fetch("/me", {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` },
      });

    if (response.ok) {
      window.location.href = "/"
    }
  }
    
  else {

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

      // successful user login -> assign JWT 
      const token = data.token
      localStorage.setItem("token", token)


      window.location.href = "/menu"; // home page will be implemented later 
    } catch (err) {
      alert("Something went wrong. Please try again.");
    }
  }
});