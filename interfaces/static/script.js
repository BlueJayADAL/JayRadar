function openTab(evt, tabName) {
  // Declare variables
  var i, tabContent, tabLinks;

  // Hide all tab content
  tabContent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabContent.length; i++) {
    tabContent[i].style.display = "none";
  }

  // Remove 'active' class from tab links
  tabLinks = document.getElementsByClassName("tab-link");
  for (i = 0; i < tabLinks.length; i++) {
    tabLinks[i].className = tabLinks[i].className.replace(" active", "");
  }

  // Show the selected tab content
  document.getElementById(tabName).style.display = "block";

  // Add 'active' class to the clicked tab link
  evt.currentTarget.className += " active";
}

document.addEventListener("DOMContentLoaded", () => {
  const configDropdown = document.getElementById("none/config");
  const saveButton = document.getElementById("saveButton");
  const resetButton = document.getElementById("resetButton");
  const socket = new WebSocket(`ws://${location.host}/ws`);
  // Set the first tab as active by default
  document.getElementsByClassName("tab-link")[0].click();

  socket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  const sendMessage = (key, value) => {
    const formattedMessage = `${key}/${value}`;
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
        if (key == "videoSource") {
          videoFeedImg.src = value
        }
      }
    }
  };

  document.addEventListener("input", handleInputEvent);
  socket.addEventListener("message", handleSocketMessage);

  saveButton.addEventListener("click", () => {
    const key = "none/save";
    const value = configDropdown.value;
    sendMessage(key, value);
    console.log("WebSocket connection established.");
  });

  resetButton.addEventListener("click", () => {
    const key = "none/config";
    const value = configDropdown.value;
    console.log("WebSocket connection established.");
    sendMessage(key, value);
  });
});