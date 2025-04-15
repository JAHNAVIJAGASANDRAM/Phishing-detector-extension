<<<<<<< HEAD
document.addEventListener('DOMContentLoaded', function() {
    const statusDiv = document.getElementById('status');
    const featureList = document.getElementById('feature-list');
    
    console.log('Popup opened, analyzing current tab...');
    
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const currentUrl = tabs[0].url;
        console.log('Current URL:', currentUrl);
        analyzeUrl(currentUrl);
    });

    // Listen for error messages from content script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === "analysisError") {
            statusDiv.className = 'status danger';
            statusDiv.textContent = 'Error: ' + message.error;
            console.error('Analysis error:', message.error);
        }
    });
});

function analyzeUrl(url) {
    const statusDiv = document.getElementById('status');
    const featureList = document.getElementById('feature-list');
    
    console.log('Starting analysis for URL:', url);
    statusDiv.className = 'status loading';
    statusDiv.textContent = 'Analyzing website...';
    
    fetch('http://localhost:5001/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: url})
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
            statusDiv.className = 'status danger';
            statusDiv.textContent = '⚠️ Warning: This might be a phishing website! (' + 
                                  Math.round(data.phishing_probability * 100) + '% probability)';
        } else {
            statusDiv.className = 'status safe';
            statusDiv.textContent = '✅ This website appears to be safe (' + 
                                  Math.round((1 - data.phishing_probability) * 100) + '% confidence)';
        }
        
        // Display features
        featureList.innerHTML = '<h4>Analysis Details:</h4>';
        Object.entries(data.features).forEach(([key, value]) => {
            const li = document.createElement('li');
            li.textContent = `${key.replace(/_/g, ' ')}: ${value}`;
            featureList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error during analysis:', error);
        statusDiv.className = 'status danger';
        statusDiv.textContent = 'Error analyzing website. Please make sure the backend server is running (http://localhost:5001).';
        featureList.innerHTML = '<p>Error details: ' + error.message + '</p>';
    });
} 
=======
document.getElementById("scan").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.runtime.sendMessage({ url: tabs[0].url });
    });
});
>>>>>>> ff9885b410f2d1ed67b1e149faeefc59cac6fd53
