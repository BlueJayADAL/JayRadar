document.addEventListener("DOMContentLoaded", () => {
  const messagesDiv = document.getElementById("messages");
  const messageForm = document.getElementById("message-form");
  const userInput = document.getElementById("user-input");
  const messageInput = document.getElementById("message-input");

  const socket = new WebSocket(`ws://${location.host}/ws`);

  socket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  socket.onmessage = (event) => {
    const message = event.data;
    messagesDiv.innerHTML += `<p>${message}</p>`;
  };

  messageForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const user = userInput.value;
    const message = messageInput.value;
    const formattedMessage = `${user}: ${message}`;
    socket.send(formattedMessage);
    messageInput.value = "";
  });
});