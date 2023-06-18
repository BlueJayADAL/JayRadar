document.addEventListener("DOMContentLoaded", () => {
    const messagesDiv = document.getElementById("messages");
    const messageForm = document.getElementById("message-form");
    const userInput = document.getElementById("user-input");
    const messageInput = document.getElementById("message-input");
    const sliders = document.querySelectorAll('input[type="range"]');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  
    const socket = new WebSocket(`ws://${location.host}/ws`);
  
    socket.onopen = () => {
      console.log("WebSocket connection established.");
    };
  
    const sendMessage = (user, message) => {
      const formattedMessage = `${user}: ${message}`;
      socket.send(formattedMessage);
      messageInput.value = "";
    };
  
    messageForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const user = userInput.value;
      const message = messageInput.value;
      sendMessage(user, message);
    });
  
    sliders.forEach(slider => {
      const sliderValue = document.getElementById(`${slider.id}Value`);
      sliderValue.textContent = slider.value;
  
      slider.addEventListener('input', (event) => {
        event.preventDefault();
        const key = slider.id;
        const value = slider.value;
        sendMessage(key, value);
      });
  
      socket.addEventListener('message', (event) => {
        const receivedMessage = event.data;
        const [key, value] = receivedMessage.split(": ");
        if (key === slider.id) {
          slider.value = value;
          sliderValue.textContent = value;
        }
      });
    });
  
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', (event) => {
        const key = checkbox.id;
        const value = checkbox.checked;
        sendMessage(key, value);
      });
  
      socket.addEventListener('message', (event) => {
        const receivedMessage = event.data;
        const [key, value] = receivedMessage.split(": ");
        const checkbox = document.getElementById(key);
        if (checkbox) {
          checkbox.checked = value === 'true';
        }
      });
    });
  });
  