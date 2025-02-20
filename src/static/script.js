document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-query").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const query = document.getElementById("user-query").value.trim();
    if (query === "") return;

    displayMessage(query, "user");
    document.getElementById("user-query").value = "";

    // Show loading indicator
    const loadingMessage = displayMessage("Bot is thinking...", "bot", []);
    document.getElementById("loading").style.display = "block";

    fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
    })
    .then((response) => response.json())
    .then((data) => {
        document.getElementById("loading").style.display = "none";
        loadingMessage.remove();  // Remove "Bot is thinking..." message
        displayMessage(data.answer, "bot", data.retrieved_context);
    })
    .catch((error) => {
        document.getElementById("loading").style.display = "none";
        loadingMessage.remove();
        displayMessage("Sorry, there was an error. Please try again later.", "bot");
    });
}

function displayMessage(message, sender, context = []) {
    const chatBox = document.getElementById("chat-box");

    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message-container", sender === "user" ? "user-message" : "bot-message");

    const messageText = document.createElement("div");
    messageText.classList.add("message-text");
    messageText.textContent = message;

    messageContainer.appendChild(messageText);
    chatBox.appendChild(messageContainer);

    if (context.length > 0) {
        const contextContainer = document.createElement("div");
        contextContainer.classList.add("context-text");
        contextContainer.innerHTML = `<strong>Context:</strong> ${context.join(", ")}`;
        messageContainer.appendChild(contextContainer);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
    return messageContainer;
}
