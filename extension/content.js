<<<<<<< HEAD
// Analyze the current page as soon as it loads
console.log('Phishing detector content script running...');
console.log('Analyzing URL:', window.location.href);

fetch('http://localhost:5001/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({url: window.location.href})
})
.then(response => {
    console.log('Response status:', response.status);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log('Analysis result:', data);
    if (data.is_phishing) {
        showPhishingWarning(data.phishing_probability);
    }
})
.catch(error => {
    console.error('Error during analysis:', error);
    chrome.runtime.sendMessage({
        action: "analysisError",
        error: error.message
    });
});

function showPhishingWarning(probability) {
    // Create and show warning banner
    const banner = document.createElement('div');
    banner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: #f44336;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 16px;
        font-family: Arial, sans-serif;
        z-index: 999999;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    `;
    
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '✕';
    closeButton.style.cssText = `
        float: right;
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0 10px;
        font-size: 20px;
    `;
    closeButton.onclick = () => banner.remove();
    
    const warningText = document.createElement('span');
    warningText.innerHTML = `⚠️ Warning: This website has been detected as a potential phishing site! (${Math.round(probability * 100)}% probability)`;
    
    banner.appendChild(warningText);
    banner.appendChild(closeButton);
    document.body.insertBefore(banner, document.body.firstChild);

    // Notify background script to update icon
    chrome.runtime.sendMessage({
        action: "updateIcon",
        isPhishing: true
    });
} 
=======
chrome.runtime.sendMessage({ url: window.location.href }, function (response) {
    console.log("Response received:", response);
});
>>>>>>> ff9885b410f2d1ed67b1e149faeefc59cac6fd53
