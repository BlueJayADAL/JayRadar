document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('input[type="range"]');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const textbox = document.getElementById('class');
    const submitButton = document.getElementById('submitButton');
    const videoFeed = document.getElementById('videoFeed');

    // Update slider values immediately
    sliders.forEach(slider => {
        const sliderValue = document.getElementById(`${slider.id}Value`);
        sliderValue.textContent = slider.value;

        slider.addEventListener('input', () => {
            sliderValue.textContent = slider.value;
            sendSliderValue(slider.id, parseFloat(slider.value));
        });
    });

    // Update checkbox values immediately
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            sendCheckboxValue(checkbox.id, checkbox.checked);
        });
    });

    // Submit textbox value on button click
    submitButton.addEventListener('click', () => {
        sendTextboxValue(textbox.id, textbox.value);
    });

    // Fetch updated video feed periodically
    setInterval(() => {
        videoFeed.src = "/video_feed";
    }, 1000);

    // Functions to send values to the server
    async function sendSliderValue(key, value) {
        const response = await fetch('/sliders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key: key,
                value: value
            })
        });
        const data = await response.json();
        console.log(data);
    }

    async function sendCheckboxValue(key, value) {
        const response = await fetch('/checkboxes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key: key,
                value: value
            })
        });
        const data = await response.json();
        console.log(data);
    }

    async function sendTextboxValue(key, value) {
        const response = await fetch('/textboxes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key: key,
                value: value
            })
        });
        const data = await response.json();
        console.log(data);
    }
});
