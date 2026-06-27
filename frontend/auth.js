async function executeAuth(event) {
    event.preventDefault();
    
    const regId = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const statusText = document.getElementById("displayStatus");
    
    statusText.style.color = "#34495e";
    statusText.textContent = "Verifying with AI-Sentinel Core...";

    try {
        const response = await fetch("http://127.0.0.1:3000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ registration_id: regId, password: password })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            statusText.style.color = "#2ecc71";
            statusText.textContent = "Access Granted! Redirecting...";
            
            // Store user session token/metadata
            localStorage.setItem("userToken", data.token);
            
            setTimeout(() => {
                window.location.href = "home.html";
            }, 1000);
        } else {
            statusText.style.color = "#e74c3c";
            statusText.textContent = data.detail || "Invalid credentials. Access Denied.";
        }
    } catch (error) {
        statusText.style.color = "#e74c3c";
        statusText.textContent = "Cannot connect to security backend engine.";
    }
}