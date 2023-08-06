import React, { useEffect, useRef, useState } from "react";
import "../css/columns.css";
import "../css/settings.css";
import "../css/styles.css";
import "../css/tabs.css";

// FYI - this is a temporary component that will be removed later.
// this will be used while we build and improve the rest of the UI.
// The CSS files imported above will also be removed later.

let socket = null;

const JayRadar = () => {
	const [currentTab, setCurrentTab] = useState("tab1");
	const configSelect = useRef(null);

	useEffect(() => {
		socket = new WebSocket(`ws://${location.host}/ws`);

		socket.onopen = () => {
			console.log("WebSocket connection established.");
		};

		document.addEventListener("input", handleInputEvent);
		socket.addEventListener("message", handleSocketMessage);

		return () => {
			socket.close();
		};
	}, []);

	const handleInputEvent = (event) => {
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
					videoFeedImg.src = value;
				}
			}
		}
	};

	const sendMessage = (key, value) => {
		const formattedMessage = `${key}/${value}`;
		socket.send(formattedMessage);
	};

	const getTabClasses = (tabName) => {
		return ["tab-link", currentTab === tabName ? "active" : ""].join(" ");
	};

	const save = () => {
		const key = "none/save";
		const value = configSelect.current.value;
		sendMessage(key, value);
	};

	const reset = () => {
		const key = "none/config";
		const value = configSelect.current.value;
		sendMessage(key, value);
	};

	return (
		<>
			<header>
				<h1>JayRadar</h1>
			</header>

			<main class="column-container">
				<div class="column-container left-column">
					<div class="config-controls">
						<div>
							<select id="none/config" ref={configSelect}>
								<option value="default">Config: Default</option>
								<option value="0">Config: 0</option>
								<option value="1">Config: 1</option>
								<option value="2">Config: 2</option>
								<option value="3">Config: 3</option>
								<option value="4">Config: 4</option>
								<option value="5">Config: 5</option>
								<option value="6">Config: 6</option>
								<option value="7">Config: 7</option>
								<option value="8">Config: 8</option>
								<option value="9">Config: 9</option>
							</select>
						</div>
						<button id="resetButton" onClick={reset}>
							Reset
						</button>
						<button id="saveButton" onClick={save}>
							Save
						</button>
					</div>
					<div class="tabs">
						<button class={getTabClasses("tab1")} onClick={() => setCurrentTab("tab1")}>
							RGB
						</button>
						<button class={getTabClasses("tab2")} onClick={() => setCurrentTab("tab2")}>
							HSV
						</button>
						<button class={getTabClasses("tab3")} onClick={() => setCurrentTab("tab3")}>
							Yolov8
						</button>
					</div>
					<div class="tab-contents">
						{currentTab === "tab1" && (
							<div id="tab1" class="tab-content">
								<div>
									<input type="checkbox" id="rgb/active" name="rgb/active" />
									<label for="rgb/active">Active</label>
								</div>
								<div class="sliders">
									<div>
										<label for="rgb/red">Red Balance:</label>
										<input
											type="range"
											id="rgb/red"
											name="rgb/red"
											min="-255"
											max="255"
											step="5"
										/>
										<span id="rgb/redValue">0</span>
									</div>
									<div>
										<label for="rgb/green">Green Balance:</label>
										<input
											type="range"
											id="rgb/green"
											name="rgb/green"
											min="-255"
											max="255"
											step="5"
										/>
										<span id="rgb/greenValue">0</span>
									</div>
									<div>
										<label for="rgb/blue">Blue Balance:</label>
										<input
											type="range"
											id="rgb/blue"
											name="rgb/blue"
											min="-255"
											max="255"
											step="5"
										/>
										<span id="rgb/blueValue">0</span>
									</div>
								</div>
							</div>
						)}
						{currentTab === "tab2" && (
							<div id="tab2" class="tab-content">
								<div>
									<input type="checkbox" id="hsv/active" name="hsv/active" />
									<label for="hsv/active">Active</label>
								</div>
								<div class="sliders">
									<div>
										<label for="hsv/saturation">Saturation:</label>
										<input
											type="range"
											id="hsv/saturation"
											name="hsv/saturation"
											min="0"
											max="10"
											step=".1"
										/>
										<span id="hsv/saturationValue">1.0</span>
									</div>
									<div>
										<label for="hsv/contrast">Contrast:</label>
										<input
											type="range"
											id="hsv/contrast"
											name="hsv/contrast"
											min="0"
											max="10"
											step=".1"
										/>
										<span id="hsv/contrastValue">1</span>
									</div>
									<div>
										<label for="hsv/brightness">Brightness:</label>
										<input
											type="range"
											id="hsv/brightness"
											name="hsv/brightness"
											min="-255"
											max="255"
											step="5"
										/>
										<span id="hsv/brightnessValue">0</span>
									</div>
								</div>
							</div>
						)}
						{currentTab === "tab3" && (
							<div id="tab3" class="tab-content">
								<div class="neural_checkboxes">
									<div>
										<input type="checkbox" id="dl/active" name="dl/active" />
										<label for="dl/active">Active</label>
									</div>
									<div>
										<input type="checkbox" id="dl/ss" name="dl/ss" />
										<label for="dl/ss">SS</label>
									</div>
									<div>
										<input type="checkbox" id="dl/ssd" name="dl/ssd" />
										<label for="dl/ssd">SSD</label>
									</div>
									<div>
										<input type="checkbox" id="dl/half" name="dl/half" />
										<label for="dl/half">Half Precision</label>
									</div>
								</div>
								<div class="sliders">
									<div>
										<label for="dl/conf">Conf:</label>
										<input
											type="range"
											id="dl/conf"
											name="dl/conf"
											min="0"
											max="1"
											step=".01"
										/>
										<span id="dl/confValue">0</span>
									</div>
									<div>
										<label for="dl/iou">IOU:</label>
										<input
											type="range"
											id="dl/iou"
											name="dl/iou"
											min="0"
											max="1"
											step=".01"
										/>
										<span id="dl/iouValue">0</span>
									</div>
									<div>
										<label for="dl/max">Max:</label>
										<input
											type="range"
											id="dl/max"
											name="dl/max"
											min="0"
											max="100"
											step="1"
										/>
										<span id="dl/maxValue">0</span>
									</div>
									<div>
										<label for="dl/img">Img:</label>
										<input
											type="range"
											id="dl/img"
											name="dl/img"
											min="160"
											max="640"
											step="32"
										/>
										<span id="dl/imgValue">160</span>
									</div>
								</div>
							</div>
						)}
					</div>
				</div>
				<div class="column-container right-column">
					<div class="video-container">
						<img id="videoFeed" src="video_feed" width="480" height="320" />
					</div>
				</div>
			</main>
		</>
	);
};

export default JayRadar;
