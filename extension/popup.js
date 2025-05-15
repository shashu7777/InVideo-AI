 let flag="false";
 document.addEventListener("DOMContentLoaded", () => {
  flag="true"
  addMessageToChat("How can I help you?", "ai-message");
});

document.getElementById("sendBtn").addEventListener("click", async () => {
  const input = document.getElementById("userInput");
  const query = input.value.trim();
  const currentFlag = flag;
  flag = "false";

  console.log("current flag=",currentFlag)

  if (!query) return;

  // Add user message to chat
  addMessageToChat(query, "user-message");

  input.value = "";
 

  // Show typing animation
  const chatBox = document.getElementById("chatBox");
  const loadingMsg = document.createElement("div");
  loadingMsg.className = "message ai-message";
  loadingMsg.innerHTML = `<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>`;
  chatBox.appendChild(loadingMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const activeTab = tabs[0];
    const url = activeTab.url;
    const urlParams = new URLSearchParams(new URL(url).search);
    const videoId = urlParams.get("v");
    //  const videoId="xAt1xcC6qfM&t=100s"

    console.log("Extracted videoId:", videoId);

    try {
      const response = await fetch(`http://localhost:5000/query/${currentFlag}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query, videoId })
      });

      const data = await response.json();
      const aiReply = data.answer;

      // Replace typing dots with actual AI response
      loadingMsg.innerText = aiReply;
    } catch (error) {
      loadingMsg.innerText = "Error communicating with AI.";
      console.error(error);
    }
  });
});

function addMessageToChat(message, className) {
  const chatBox = document.getElementById("chatBox");
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${className}`;
  msgDiv.innerText = message;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

