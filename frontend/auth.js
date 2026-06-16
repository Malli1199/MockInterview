function validateCredentials(user, pass) {
    if (!user || !pass) {
        return "Missing Input Fields";
    }
    if (user === "malli" && pass === "malli1199") {
        return "Auth Verified";
    }
    return "Invalid Access ID";
}

// 1. Pass the 'event' object into the function
function executeAuth(event) {
    // 2. Prevent the page from refreshing automatically
    if (event) {
        event.preventDefault(); 
    }

    const userElement = document.getElementById("username").value;
    const passElement = document.getElementById("password").value;
    const statusBox = document.getElementById("displayStatus");
    
    const outcome = validateCredentials(userElement, passElement);
    if (outcome === "Auth Verified") {
        // 3. Use an absolute-relative path assignment to prevent routing issues
        window.location.assign("./home.html");
    } else {
        statusBox.style.color = "#c0392b";
        statusBox.innerText = outcome;
    }
}