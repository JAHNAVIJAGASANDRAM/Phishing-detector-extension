// Function to analyze the current webpage
async function analyzeWebpage() {
    try {
        const url = window.location.href;
        console.log('Analyzing URL:', url);

        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            credentials: 'omit',
            body: JSON.stringify({ url: url })
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Analysis result:', data);
        
        if (data.is_phishing) {
            showPhishingWarning(data);
        }
    } catch (error) {
        console.error('Error during analysis:', error);
        // Send error to background script
        chrome.runtime.sendMessage({
            action: "analysisError",
            error: error.message || "Failed to analyze website"
        });
    }
}

// Function to show phishing warning
function showPhishingWarning(data) {
    // Remove existing warning if any
    const existingWarning = document.getElementById('phishing-warning-banner');
    if (existingWarning) {
        existingWarning.remove();
    }

    const warningBanner = document.createElement('div');
    warningBanner.id = 'phishing-warning-banner';
    warningBanner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #ff4444;
        color: white;
        padding: 15px;
        text-align: left;
        font-size: 16px;
        z-index: 999999;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    `;

    // Create warning content
    let warningContent = `⚠️ Warning: This website has been detected as potentially dangerous!<br>`;
    warningContent += `<strong>Confidence:</strong> ${Math.round(data.confidence * 100)}%<br>`;

    // Add external API results if available
    if (data.external_checks) {
        if (data.external_checks.phishtank && data.external_checks.phishtank.is_phishing) {
            warningContent += `<br>✖️ This URL is listed in PhishTank's database of known phishing sites.<br>`;
        }
        if (data.external_checks.google_safe_browsing && data.external_checks.google_safe_browsing.is_dangerous) {
            warningContent += `<br>⚠️ Google Safe Browsing has flagged this site as dangerous.<br>`;
            if (data.external_checks.google_safe_browsing.threat_types) {
                warningContent += `Threat types: ${data.external_checks.google_safe_browsing.threat_types.join(', ')}<br>`;
            }
        }
    }

    // Add risk factors if available
    if (data.risk_factors && data.risk_factors.length > 0) {
        warningContent += `<br><strong>Risk Factors:</strong><br>`;
        warningContent += `<ul style="margin: 5px 0; padding-left: 20px;">`;
        data.risk_factors.forEach(factor => {
            warningContent += `<li>${factor}</li>`;
        });
        warningContent += `</ul>`;
    }

    // Add dismiss button
    warningContent += `
        <button onclick="this.parentElement.remove()" style="
            margin-top: 10px;
            padding: 5px 10px;
            border: none;
            border-radius: 3px;
            background: white;
            cursor: pointer;
            font-weight: bold;
        ">Dismiss Warning</button>
    `;

    warningBanner.innerHTML = warningContent;
    document.body.insertBefore(warningBanner, document.body.firstChild);
}

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analyze") {
        analyzeWebpage();
    }
    return true;
});

// Analyze when the page loads
console.log('Content script loaded, starting analysis...');
analyzeWebpage();
