let conversationHistory = [];

function updateConversation(msg, isUser) {
    let formattedMsg = (isUser ? "User: " : "Bot: ") + msg;
    conversationHistory.push(formattedMsg);

    // Keep only the last N interactions, if necessary
    const maxHistorySize = 10;  // Example size
    if (conversationHistory.length > maxHistorySize) {
        conversationHistory.shift(); // Remove the oldest interaction
    }

    // Update textarea content
    document.getElementById("conversation").value = conversationHistory.join("\n");
}

function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    updateConversation(userInput, true);

    // Disable buttons and show loading indicator
    document.getElementById("sendButton").disabled = true;
    document.getElementById("resetButton").disabled = true;
    document.getElementById("conversation").classList.add("loading");

    const fullPrompt = conversationHistory.join("\n") + "\nBot: ";
    const baseUrl = window.location.origin;
    fetch(`${baseUrl}/generate/?prompt=${encodeURIComponent(fullPrompt)}`)
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

    // Clear the textarea content
    document.getElementById("conversation").value = "";
}

window.onload = () => {
    document.getElementById("userInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
}

