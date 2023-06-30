document.addEventListener("DOMContentLoaded", () => {
  const debuggingForm = document.getElementById("debugging-form");
  const keyInput = document.getElementById("key-input");
  const valueInput = document.getElementById("value-input");
  const configDropdown = document.getElementById("config");
  const saveButton = document.getElementById("saveButton");
  const resetButton = document.getElementById("resetButton");
  const socket = new WebSocket(`ws://${location.host}/ws`);

  socket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  const sendMessage = (key, value) => {
    const formattedMessage = `${key}: ${value}`;
    socket.send(formattedMessage);
  };

  const handleInputEvent = (event) => {
    event.preventDefault();
    const element = event.target;
    const key = element.id;
    let value;

    if (element.type === "range") {
      value = element.value;
    } else if (element.type === "checkbox") {
      value = element.checked;
    } else if (element.type === "select-one") {
      value = element.value;
    }

    sendMessage(key, value);
  };

  const handleSocketMessage = (event) => {
    const receivedMessage = event.data;
    const [key, receivedValue] = receivedMessage.split(": ");
    const value = receivedValue.toLowerCase();

    const element = document.getElementById(key);
    if (element) {
      if (element.type === "range") {
        element.value = value;
        const sliderValue = document.getElementById(`${key}Value`);
        if (sliderValue) {
          sliderValue.textContent = value;
        }
      } else if (element.type === "checkbox") {
        element.checked = value === "true";
      } else if (element.type === "select-one") {
        element.value = value;
      }
    }
  };

  document.addEventListener("input", handleInputEvent);
  socket.addEventListener("message", handleSocketMessage);

  saveButton.addEventListener("click", () => {
    const key = "save_config";
    const value = configDropdown.value;
    sendMessage(key, value);
  });

  resetButton.addEventListener("click", () => {
    const key = "config";
    const value = configDropdown.value;
    sendMessage(key, value);
  });
});
