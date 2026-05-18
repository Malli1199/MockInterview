function validateLogin(username, password) {
    // Basic structural validation rules
    if (!username || !password) {
        return "Fields cannot be empty";
    }
    
    // Core verification logic
    if (username === "student" && password === "mock2026") {
        return "Login Successful! Redirecting to Interview Panels...";
    } else {
        return "Invalid Credentials. Try again.";
    }
}

function handleLogin() {
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;
    const msgElement = document.getElementById("message");
    
    const result = validateLogin(user, pass);
    
    if (result.includes("Successful")) {
        msgElement.style.color = "green";
    } else {
        msgElement.style.color = "red";
    }
    msgElement.innerText = result;
}

// Exporting module cleanly so testing frameworks can read it if needed
if (typeof module !== 'undefined') {
    module.exports = { validateLogin };
}