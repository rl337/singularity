let conversationHistory = [];

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

    // Create a new div for the message
    let messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isUser ? "user-message" : "service-response");
    messageDiv.innerHTML = displayMsg; // Use innerHTML to render the display message

    // Append the new message div to the conversation container
    let conversationDiv = document.getElementById("conversation");
    conversationDiv.appendChild(messageDiv);

    // Scroll to the newest message
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

// Function to escape HTML characters in messages
function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
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
    const baseUrl = window.location.origin;
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: fullPrompt, max_request_length: 100 }) // Adjust max_request_length as needed
    };

    fetch(`${baseUrl}/generate/`, requestOptions)  // Make sure the URL is correct
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

window.onload = () => {
    document.getElementById("userInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
}

