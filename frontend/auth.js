function validateCredentials(user, pass) {
    if (!user || !pass) {
        return "Missing Input Fields";
    }
    // Matching your credentials: malli / malli1199
    if (user === "malli" && pass === "malli1199") {
        return "Auth Verified";
    }
    return "Invalid Access ID";
}

function executeAuth(event) {
    // Prevent the form from refreshing the page and killing the JS execution loop
    if (event) {
        event.preventDefault(); 
    }

    const userElement = document.getElementById("username").value;
    const passElement = document.getElementById("password").value;
    const statusBox = document.getElementById("displayStatus");
    
    const outcome = validateCredentials(userElement, passElement);
    
    if (outcome === "Auth Verified") {
        // Clear any old error styling
        statusBox.innerText = "";
        
        // BULLETPROOF LOCAL REDIRECTION:
        // Swapping to direct .href assignment forces the browser to drop 'index.html' 
        // and load 'home.html' inside the exact same folder context.
        window.location.href = "home.html";
    } else {
        statusBox.style.color = "#c0392b";
        statusBox.innerText = outcome;
    }
}