/* eslint-disable no-restricted-globals */
import { useEffect, useRef } from 'react';
import '../css/columns.css';
import '../css/settings.css';
import '../css/styles.css';
import '../css/tabs.css';

// FYI - this is a temporary component that will be removed later.
// this will be used while we build and improve the rest of the UI.
// The CSS files imported above will also be removed later.

let socket: WebSocket | null = null;

/**
 * Temporary component that renders the entire UI.
 */
function JayRadar() {
  const configSelect = useRef<HTMLSelectElement>(null);

  useEffect(() => {
    socket = new WebSocket(`ws://${location.host}/ws`);

    /**
     * Handles the WebSocket connection being established.
     */
    socket.onopen = () => {
      console.log('WebSocket connection established.');
    };

    document.addEventListener('input', handleInputEvent);
    socket.addEventListener('message', handleSocketMessage);

    return () => {
      socket?.close();
    };
  }, []);

  /**
   * Handles input events from the user.
   */
  const handleInputEvent = (event: Event) => {
    const element = event.target as HTMLInputElement;
    const key = element.id;
    let value;

    if (element.type === 'range') {
      value = element.value;
    } else if (element.type === 'checkbox') {
      value = element.checked;
    } else if (element.type === 'select-one') {
      value = element.value;
    }

    sendMessage(key, value?.toString() || '');
  };

  /**
   * Handles messages received from the server.
   */
  const handleSocketMessage = (event: MessageEvent) => {
    const receivedMessage = event.data;
    const [key, receivedValue] = receivedMessage.split(': ');
    const value = receivedValue.toLowerCase();

    const element = document.getElementById(key) as HTMLInputElement;
    if (element) {
      if (element.type === 'range') {
        element.value = value;
        const sliderValue = document.getElementById(`${key}Value`);
        if (sliderValue) {
          sliderValue.textContent = value;
        }
      } else if (element.type === 'checkbox') {
        element.checked = value === 'true';
      } else if (element.type === 'select-one') {
        element.value = value;
        if (key === 'videoSource') {
          // videoFeedImg.src = value;
        }
      }
    }
  };

  /**
   * Sends a message to the server.
   */
  const sendMessage = (key: string, value: string) => {
    const formattedMessage = `${key}/${value}`;
    socket?.send(formattedMessage);
  };

  /**
   * Saves the current config.
   */
  const save = () => {
    const key = 'none/save';
    const { value } = configSelect.current as HTMLSelectElement;
    sendMessage(key, value);
  };

  /**
   * Resets the config to the default values.
   */
  const reset = () => {
    const key = 'none/config';
    const { value } = configSelect.current as HTMLSelectElement;
    sendMessage(key, value);
  };

  /**
   * Changes the tab that is displayed.
   */
  const changeTab = (tabName: string) => {
    const tabs = ['tab1', 'tab2', 'tab3'];

    tabs.forEach((tab) => {
      const tabElement = document.getElementById(tab) as HTMLElement;
      const tabLinkElement = document.getElementById(`${tab}-link`) as HTMLElement;

      if (tab === tabName) {
        tabElement.classList.remove('hidden');
        tabLinkElement.classList.add('active');
      } else {
        tabElement.classList.add('hidden');
        tabLinkElement.classList.remove('active');
      }
    });
  };

  return (
    <>
      <header>
        <h1>JayRadar</h1>
      </header>

      <main className="column-container">
        <div className="column-container left-column">
          <div className="config-controls">
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
            <button id="resetButton" onClick={reset} type="button">
              Reset
            </button>
            <button id="saveButton" onClick={save} type="button">
              Save
            </button>
          </div>
          <div className="tabs">
            <button
              id="tab1-link"
              className="tab-link active"
              onClick={() => changeTab('tab1')}
              type="button"
            >
              RGB
            </button>
            <button id="tab2-link" className="tab-link" onClick={() => changeTab('tab2')} type="button">
              HSV
            </button>
            <button id="tab3-link" className="tab-link" onClick={() => changeTab('tab3')} type="button">
              Yolov8
            </button>
          </div>
          <div className="tab-contents">
            <div id="tab1" className="tab-content">
              <div>
                <input type="checkbox" id="rgb/active" name="rgb/active" />
                <label htmlFor="rgb/active">Active</label>
              </div>
              <div className="sliders">
                <div>
                  <label htmlFor="rgb/red">Red Balance:</label>
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
                  <label htmlFor="rgb/green">Green Balance:</label>
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
                  <label htmlFor="rgb/blue">Blue Balance:</label>
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
            <div id="tab2" className="tab-content hidden">
              <div>
                <input type="checkbox" id="hsv/active" name="hsv/active" />
                <label htmlFor="hsv/active">Active</label>
              </div>
              <div className="sliders">
                <div>
                  <label htmlFor="hsv/saturation">Saturation:</label>
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
                  <label htmlFor="hsv/contrast">Contrast:</label>
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
                  <label htmlFor="hsv/brightness">Brightness:</label>
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
            <div id="tab3" className="tab-content hidden">
              <div className="neural_checkboxes">
                <div>
                  <input type="checkbox" id="dl/active" name="dl/active" />
                  <label htmlFor="dl/active">Active</label>
                </div>
                <div>
                  <input type="checkbox" id="dl/ss" name="dl/ss" />
                  <label htmlFor="dl/ss">SS</label>
                </div>
                <div>
                  <input type="checkbox" id="dl/ssd" name="dl/ssd" />
                  <label htmlFor="dl/ssd">SSD</label>
                </div>
                <div>
                  <input type="checkbox" id="dl/half" name="dl/half" />
                  <label htmlFor="dl/half">Half Precision</label>
                </div>
              </div>
              <div className="sliders">
                <div>
                  <label htmlFor="dl/conf">Conf:</label>
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
                  <label htmlFor="dl/iou">IOU:</label>
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
                  <label htmlFor="dl/max">Max:</label>
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
                  <label htmlFor="dl/img">Img:</label>
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
          </div>
        </div>
        <div className="column-container right-column">
          <div className="video-container">
            <img id="videoFeed" src="video_feed" alt="video_feed" width="480" height="320" />
          </div>
        </div>
      </main>
    </>
  );
}

export default JayRadar;
