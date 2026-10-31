const askButton = document.getElementById("ask-button");
const responseArea = document.getElementById("response");

askButton.addEventListener("click", async function () {

    const message = messageInput.value.trim();

    if (!message) {
        responseArea.textContent = "Please enter a message.";
        return;
    }

    responseArea.textContent = "Thinking...";
    askButton.disabled = true;

    try {

        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (data.error) {
            responseArea.textContent = "Error: " + data.error;
            return;
        }

        responseArea.textContent = data.response;
        messageInput.value = "";

    } catch (error) {

        responseArea.textContent =
            "Something went wrong. Please try again.";

        console.error(error);

    } finally {
        askButton.disabled = false;
    }
});