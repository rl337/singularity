function generateText() {
    const inputPrompt = document.getElementById('inputPrompt').value;
    // Use window.location.origin to get the base URL dynamically
    const baseUrl = window.location.origin;
    fetch(`${baseUrl}/generate/?prompt=${encodeURIComponent(inputPrompt)}`)
        .then(response => response.json())
        .then(data => document.getElementById('outputText').innerText = data.generated_text)
        .catch(error => console.error('Error:', error));
}

