const marked = require('marked');
const DOMPurify = require('dompurify')(window); // Assuming you're in a browser environment
import 'github-markdown-css';

let conversationHistory = [];

// Assuming your API service runs on port 8000
const apiPort = 8000;

// Extract hostname and protocol from window.location.origin
const {protocol, hostname} = window.location;

// Construct the base URL for the API service
const serviceBaseUrl = `${protocol}//${hostname}:${apiPort}`;

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;")
        .replace(/</g, "&lt;") // Escape opening angle brackets
        .replace(/>/g, "&gt;"); // Escape closing angle brackets
}

function updateConversation(msg, isUser) {
    let formattedMsg = (isUser ? "<human>: " : "<bot>: ") + msg;
    conversationHistory.push(formattedMsg);

    // Keep only the last N interactions, if necessary
    const maxHistorySize = 10; // Example size
    if (conversationHistory.length > maxHistorySize) {
        conversationHistory.shift(); // Remove the oldest interaction
    }

    // Construct the display message with emoji
    let displayMsg = (isUser ? "😊: " : "🤖: ") + escapeHtml(msg);

    let htmlContent = marked.parse(displayMsg);
    let safeHtmlContent = DOMPurify.sanitize(htmlContent);

    // Create the outer div for the message
    let messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isUser ? "user-message" : "service-response");
    
    // Create the inner div specifically for the markdown content
    let markdownDiv = document.createElement("div");
    markdownDiv.classList.add("markdown-body");
    markdownDiv.innerHTML = safeHtmlContent; // Render the markdown content here

    // Append the markdown div to the message div
    messageDiv.appendChild(markdownDiv);

    // Append the new message div to the conversation container
    let conversationDiv = document.getElementById("conversation");
    conversationDiv.appendChild(messageDiv);

    // Scroll to the newest message
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}


function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    updateConversation(userInput, true);

    // Disable buttons and show loading indicator
    document.getElementById("sendButton").disabled = true;
    document.getElementById("resetButton").disabled = true;
    document.getElementById("conversation").classList.add("loading");

    const fullPrompt = conversationHistory.join("\n") + "\n<bot>: ";

    let customParameters = {};
    document.querySelectorAll('#ModelParams input').forEach(input => {
        // Convert numerical values to numbers to ensure proper JSON formatting
        customParameters[input.id] = isNaN(input.value) ? input.value : Number(input.value);
    });

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            prompt: fullPrompt,
            ...customParameters // Spread the custom parameters here
        }) 
    };

    fetch(`${serviceBaseUrl}/generate/`, requestOptions)  // Make sure the URL is correct
        .then(response => response.json())
        .then(data => {
            updateConversation(data.generated_text, false);
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            // Re-enable buttons and remove loading indicator
            document.getElementById("sendButton").disabled = false;
            document.getElementById("resetButton").disabled = false;
            document.getElementById("conversation").classList.remove("loading");
        });

    // Clear input field
    document.getElementById("userInput").value = "";
}

function resetConversation() {
    conversationHistory = []; // Clear the conversation history

    // Clear all child elements from the conversation container
    let conversationDiv = document.getElementById("conversation");
    while (conversationDiv.firstChild) {
        conversationDiv.removeChild(conversationDiv.firstChild);
    }
}

function fetchModelConfig() {
    // Prepare the POST request options
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Don't need to send a model parameter for the default model
        body: JSON.stringify({}) // Empty body or relevant details if required by the endpoint
    };

    fetch(`${serviceBaseUrl}/model_config/`, requestOptions)
        .then(response => response.json())
        .then(config => {
            populateConfigForm(config.config.args);
        })
        .catch(error => console.error('Error fetching model config:', error));
}

function populateConfigForm(args) {
    const modelParamsDiv = document.getElementById('ModelParams');
    modelParamsDiv.innerHTML = ''; // Clear previous content

    // Create form elements for each argument
    for (let key in args) {
        // Create label
        let label = document.createElement('label');
        label.innerHTML = key + ': ';
        label.htmlFor = key;
        modelParamsDiv.appendChild(label);

        // Create input field
        let input = document.createElement('input');
        input.type = 'text'; // Or 'number' if the parameter is always a number
        input.id = key;
        input.value = args[key]; // Set the current value
        modelParamsDiv.appendChild(input);

        // Add a break line
        modelParamsDiv.appendChild(document.createElement('br'));
    }
}

function openTab(tabName) {
    // Get all elements with class="tabcontent" and hide them
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Activate the tab content
    let targetTabContent = document.getElementById(tabName);
    if (targetTabContent) {
        targetTabContent.style.display = "block";
    } else {
        console.error(`No tab content found with ID '${tabName}'. Ensure the HTML structure is correct.`);
    }

    // Activate the corresponding tab link
    let tabLink = document.querySelector(`.tablinks[onclick*="'${tabName}'"]`);
    if (tabLink) {
        tabLink.classList.add("active");
    } else {
        console.error(`No tab link found for '${tabName}'. Ensure the HTML structure is correct.`);
    }

}


window.onload = () => {
    document.getElementById("userInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
    fetchModelConfig();
    openTab('ModelParams'); // Open Model Parameters tab by default
    document.querySelector(".tablinks").classList.add("active");

}

// Initialization function to set up event listeners
function initializeApp() {
    document.getElementById('sendButton').addEventListener('click', sendMessage);
    document.getElementById('resetButton').addEventListener('click', resetConversation);
}

// When the DOM is fully loaded, initialize the app
document.addEventListener('DOMContentLoaded', initializeApp);


