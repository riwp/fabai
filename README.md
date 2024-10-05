
--------------------------------------------
Install pre-requisites
--------------------------------------------
1. Update Linux
    sudo apt update

2. Install Go
    Required to install fabric
    https://go.dev/doc/install

    STEPS:
    Download latest distro:
    https://go.dev/dl/

    Copy to path:
    copy binaries to /usr/local/go/bin

    Set export path:
    export PATH=$PATH:/usr/local/go/bin

    Verify installed:
    go version

3. Install Fabric

    Modular AI framework uses crowd sourced prompts to solve problems 

    https://github.com/danielmiessler/fabric

    STEPS:
    # Linux (amd64): 
    curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-amd64 > fabric && chmod +x fabric && ./fabric --version

    # Install Fabric directly from the repo
    go install github.com/danielmiessler/fabric@latest

4. Install chromium-browser
    Used in headless mode to download web page content from a URL

    https://www.chromium.org/getting-involved/download-chromium/

    STEPS:
    Install:
    sudo apt install chromium-browser

5. Install html2text
    Used to cleanup web html content into text content

    STEPS:
    sudo apt install html2text

6. Install yt-dlp
    Used to download YouTube 

    sudo apt install yt-dlp

--------------------------------------------
Modify service files with home directory and user
--------------------------------------------
7. Modify bash/fabai_aiwebui.service replacing home directory and user name
    nano bash/fabai_aiwebui.service

    ExecStart=/usr/bin/python3 /home/[Replace User Home Directory]/fabai/aiwebui/aiwebui.py
    WorkingDirectory=/home/[Replace User Home Directory]/fabai
    User=[Replace User]

8. Modify fabai_get_ai_insights.service replacing home directory and user name
    nano bash/fabai_get_ai_insights.service

    ExecStart=/usr/bin/python3 /home/[Replace User Home Directory]/fabai/aiwebui/aiwebui.py
    WorkingDirectory=/home/[Replace User Home Directory]/fabai
    User=[Replace User]

--------------------------------------------
Add services and check status
--------------------------------------------

9. Run add_services.sh
    sudo bash/add_services.sh

10. Check status of services post installation
    sudo bash/get_status.sh

--------------------------------------------
Open Web Application
--------------------------------------------

11. Go to Web Application aiwebui on port 5000
    Open a browser and go to URL:  http://[Server Name]:5005/

    You should see something like below:
![image](https://github.com/user-attachments/assets/b856a4cf-d24d-4422-b68a-61616f0ceee2)


--------------------------------------------
Operation Type
--------------------------------------------

- Summary:  Summarizes text
- Claims:  Analyzes claims
- Keynote: creates a keynote
- MSummary: Creates a mini summary
- Essay: Creates essay
- Wisdom: My favorite and default!  Analyzes and provides Summary, Ideas, Insights, Quotes, Habits, Facts, References, Recommendations


--------------------------------------------
Web UI Functions
--------------------------------------------

Text Input: allows you to copy paste text and runs fabric AI
- Paste your text input
- Click Let's Go

AI Video: goes to youtube, gets transcript, and runs fabric AI
- Enter URL to Youtube video
- Click Let's Go

AI Web: goes to web site, downloads html, cleans up, and runs fabric AI
- Enter URL to web page to analyze
- Click Let's Go
  
--------------------------------------------
Key locations and configurations:
--------------------------------------------

- Web UI Log: aiwebui/fabai_webui.log
- API Log: fabai_api.log
- out/text: stores the AI output of text
- out/video: stores AI output for downloaded videos
- ai/web: stores the AI output for downloaded web pages
- common/fabai_common_variables.py contains variables common across aiwebui and api
- common/fabai_get_static_debug_data.py reads file system for a file and returns text, used for debugging purposes without hitting server (ie test web or other apis)

--------------------------------------------
Web UI: run on port 5005 (change AIWEBUI_PORT_NUMBER in aiwebui.py)
--------------------------------------------
- aiwebui/aiewbui.py main server side code index.html posts to.  calls fabai_get_ai_insights.py as orchestration layer
- aiwebui/templates/index.html contains the html, javascript for the UI which posts data to  aiwebui/aiewbui.py

--------------------------------------------
APIs: run on port 5006 (change API_PORT_NUMBER in fabai_common.py)
--------------------------------------------
- api/fabai_common.py common code imported across all apis
- api/fabai_get_ai_insights.py main entry point from web ui and orchestrates calls based upon web ui function selected
- api/fabai_get_fabric_insights_from_text.py takes in text, calls fabric with --pattern and returns AI output
- api/fabai_get_webpage_as_text.py downloads html from web, cleans up, and returns text
- api/fabai_get_youtubevideo_transcript.py downloads youtube transcript, and returns text

--------------------------------------------
BASH Scripts
--------------------------------------------
- fabai_aiwebui.service service configuration file copied to /etc/systemd/system/
- fabai_get_ai_insights.service configuration file copied to /etc/systemd/system/
- remove_services.sh un-installs services and removes files
- add_services.sh copies .service files and sets up service (note: home directory and user need to be set in .service files)
- get_status.sh provides status to check if services are healthy
- clean_dirs.sh cleans output directory contents
- restart_services.sh reloads and re-starts services
- restart_services.sh reloads and re-starts services

--------------------------------------------
Future Enhancements
--------------------------------------------
PDF to Text:
- sudo apt install poppler-utils
- pdftotext filename.pdf

YouTube Search
- Find topics to summarize and go summarize them

ChatGPT Agents
- Get topics and sources to analyze 

Mobile App shortcut:
- make it east to send content to web app


--------------------------------------------
Dev in progress
--------------------------------------------


Create a Chrome Extension to mire easily pass web content to web app

Step 1: Set Up Your Extension Directory

	1.	Create a New Folder: Name it something like MyChromeExtension.
	2.	Create the Required Files:
	•	Inside this folder, create the following files:
	•	manifest.json
	•	popup.html
	•	popup.js
	•	background.js (optional, for more complex interactions)

Step 2: Create manifest.json

This file is the metadata for your extension and tells Chrome how to load it.

{
  "manifest_version": 3,
  "name": "My Chrome Extension",
  "version": "1.0",
  "description": "Capture URL and page content.",
  "permissions": [
    "activeTab",
    "scripting"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon16.png",
      "48": "icon48.png",
      "128": "icon128.png"
    }
  },
  "background": {
    "service_worker": "background.js"
  }
}

Step 3: Create popup.html

This is the HTML for the extension’s popup interface.

<!DOCTYPE html>
<html>
<head>
    <title>My Chrome Extension</title>
    <script src="popup.js"></script>
</head>
<body>
    <h1>Send Page Data</h1>
    <button id="sendData">Send Data to AI Web App</button>
</body>
</html>

Step 4: Create popup.js

This script will handle capturing the URL and content of the page and sending it to your application.

document.getElementById('sendData').addEventListener('click', async () => {
    // Get the current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Get the URL and content of the current page
    const url = tab.url;
    const content = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => document.body.innerText
    });

    // Send data to your web application
    fetch('https://yourapp.com/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            url: url,
            content: content[0].result // content[0].result contains the page content
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

Step 5: Create background.js (optional)

If you want to handle background tasks or events, you can use this file. For basic operations, you might not need this yet.

Step 6: Load the Extension in Chrome

	1.	Open Chrome.
	2.	Go to chrome://extensions.
	3.	Enable Developer Mode (toggle on the top right).
	4.	Click on “Load unpacked”.
	5.	Select the folder you created for your extension (MyChromeExtension).

Step 7: Test Your Extension

	1.	Open any web page.
	2.	Click the extension icon in the toolbar.
	3.	Click the “Send Data to AI Web App” button.
	4.	Check your console for success or error messages.

Notes:

	•	Icons: You can create icons of different sizes (16x16, 48x48, 128x128 pixels) and include them in your extension directory if you want custom icons. Update the manifest.json accordingly.
	•	Permissions: Adjust permissions in the manifest.json as needed.
	•	CORS: Ensure your web application allows requests from the Chrome extension’s origin if you encounter CORS issues.

