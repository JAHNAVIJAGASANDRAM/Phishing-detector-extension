<<<<<<< HEAD
// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Phishing Detector extension installed');
});

// Background script for handling extension-wide events
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "updateIcon") {
        // Update the extension icon based on phishing detection
        const iconPath = message.isPhishing ? 
            {
                16: "icons/icon16_warning.png",
                48: "icons/icon48_warning.png",
                128: "icons/icon128_warning.png"
            } :
            {
                16: "icons/icon16.png",
                48: "icons/icon48.png",
                128: "icons/icon128.png"
            };
        
        chrome.action.setIcon({ path: iconPath });
    }
}); 
=======
function checkUrl(message, sender, sendResponse) {
    fetch("http://localhost:8080/check-url", { 
        method: "POST",
        body: JSON.stringify({ url: message.url }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => handleResponse(data, sendResponse)) 
    .catch(handleError);

    return true; 
}
function handleResponse(data, sendResponse) {
    if (data.isPhishing) {
        chrome.notifications.create({
            type: "basic",
            iconUrl: "icon.png",
            title: "Phishing Alert!",
            message: "This website may be a phishing attempt."
        });
    }
    sendResponse({ status: "done" });
}
function handleError(error) {
    console.error("Error in background.js:", error);
}
chrome.runtime.onMessage.addListener(checkUrl);
>>>>>>> ff9885b410f2d1ed67b1e149faeefc59cac6fd53
