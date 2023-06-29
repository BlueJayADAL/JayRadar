document.addEventListener("DOMContentLoaded", () => {
    const debuggingForm = document.getElementById("debugging-form");
    const keyInput = document.getElementById("key-input");
    const valueInput = document.getElementById("value-input");
//  const sliders = document.querySelectorAll('input[type="range"]');
    const spinboxes = document.querySelectorAll('input[type="number"]');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const configDropdown = document.getElementById("config");
    const saveButton = document.getElementById("saveButton");
    const resetButton = document.getElementById("resetButton");
    const socket = new WebSocket(`ws://${location.host}/ws`);
  
    socket.onopen = () => {
      console.log("WebSocket connection established.");
    };
  
    const sendMessage = (user, message) => {
      const formattedMessage = `${user}: ${message}`;
      socket.send(formattedMessage);
    };
  
    debuggingForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const user = keyInput.value;
      const message = valueInput.value;
      sendMessage(user, message);
      valueInput.value = "";
    });
/* 
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
  */
    spinBoxes.forEach(spinBox => {
      const spinBoxValue = document.getElementById(`${spinBox.id}Value`);
      spinBoxValue.textContent = spinBox.value;
    
      spinBox.addEventListener('input', (event) => {
        event.preventDefault();
        const key = spinBox.id;
        const value = spinBox.value;
        sendMessage(key, value);
      });
    
      socket.addEventListener('message', (event) => {
        const receivedMessage = event.data;
        const [key, value] = receivedMessage.split(": ");
        if (key === spinBox.id) {
          spinBox.value = value;
          spinBoxValue.textContent = value;
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
        const [key, receivedValue] = receivedMessage.split(": ");
        const value = receivedValue.toLowerCase();  // Assign the converted lowercase value to a new variable

        const checkbox = document.getElementById(key);
        if (checkbox) {
          checkbox.checked = value === 'true';
        }
      });
    });

    configDropdown.addEventListener("change", (event) => {
      const value = event.target.value;
      const key = event.target.id;
      sendMessage(key, value);
    });
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
  