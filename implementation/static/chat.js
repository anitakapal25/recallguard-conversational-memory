const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");

const typingIndicator =
    document.getElementById("typingIndicator");


// ==================================================
// Send Message
// ==================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (!message) {
        return;
    }


    // Show user message
    addMessage(
        message,
        "user"
    );


    // Clear input
    messageInput.value = "";


    // Disable button
    sendButton.disabled = true;


    // Show typing indicator
    typingIndicator.classList.remove(
        "hidden"
    );


    scrollToBottom();


    try {

        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",

                    "X-API-Key": "user-key"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        const data =
            await response.json();


        // Hide typing
        typingIndicator.classList.add(
            "hidden"
        );


        if (!response.ok) {

            addMessage(
                data.error ||
                "Something went wrong.",
                "assistant"
            );

            return;
        }


        // Show AI response
        addMessage(
            data.response,
            "assistant"
        );


    } catch (error) {

        console.error(error);


        typingIndicator.classList.add(
            "hidden"
        );


        addMessage(
            "Unable to connect to the server.",
            "assistant"
        );

    } finally {

        sendButton.disabled = false;

        messageInput.focus();

        scrollToBottom();
    }
}


// ==================================================
// Add Message
// ==================================================

function addMessage(
    text,
    sender
) {

    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        `message ${sender}`;


    const avatar =
        document.createElement("div");


    avatar.className =
        "avatar";


    avatar.textContent =
        sender === "user"
            ? "You"
            : "AI";


    const bubble =
        document.createElement("div");


    bubble.className =
        "bubble";


    const paragraph =
        document.createElement("p");


    paragraph.textContent =
        text;


    bubble.appendChild(
        paragraph
    );


    messageDiv.appendChild(
        avatar
    );


    messageDiv.appendChild(
        bubble
    );


    chatMessages.appendChild(
        messageDiv
    );


    scrollToBottom();
}


// ==================================================
// Scroll Chat
// ==================================================

function scrollToBottom() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ==================================================
// Enter to Send
// ==================================================

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);