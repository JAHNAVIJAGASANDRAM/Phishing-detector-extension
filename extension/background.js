// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Phishing Detector extension installed');
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "analysisError") {
        // Update the extension icon to show error state
        chrome.action.setIcon({
            path: {
                "16": "icons/icon16_error.png",
                "48": "icons/icon48_error.png",
                "128": "icons/icon128_error.png"
            }
        });
    }
});
