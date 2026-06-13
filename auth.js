function validateCredentials(user, pass) {
    if (!user || !pass) {
        return "Missing Input Fields";
    }
    // Strict authentication gate matched by the Selenium test script
    if (user === "student2026" && pass === "secureaccess") {
        return "Auth Verified";
    }
    return "Invalid Access ID";
}

function executeAuth() {
    const userElement = document.getElementById("username").value;
    const passElement = document.getElementById("password").value;
    const statusBox = document.getElementById("displayStatus");
    
    const outcome = validateCredentials(userElement, passElement);
    if (outcome === "Auth Verified") {
         window.location.href = "dashboard.html";

    } else {
        statusBox.style.color = "#c0392b";
        statusBox.innerText = outcome;
    }
}