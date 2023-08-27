/* eslint-disable no-restricted-globals */
import { useEffect, useRef, useState } from 'react';
import '../css/columns.css';
import '../css/settings.css';
import '../css/styles.css';
import '../css/tabs.css';
import ConfigButton from './Config/ConfigButton';
import ConfigOption from './Config/ConfigOption';
import TabLink from './Tabs/TabLink';
import RgbTab from './Tabs/RgbTab';
import HsvTab from './Tabs/HsvTab';
import Yolov8Tab from './Tabs/Yolov8Tab';
import { TabOptions } from '../types/TabOptions';

// FYI - this is a temporary component that will be removed later.
// this will be used while we build and improve the rest of the UI.
// The CSS files imported above will also be removed later.

let socket: WebSocket | null = null;

/**
 * Temporary component that renders the entire UI.
 */
function JayRadar() {
  const configSelect = useRef<HTMLSelectElement>(null);
  const configOptions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  const [currentTab, setCurrentTab] = useState('RGB');

  const [options, setOptions] = useState<TabOptions>({
    rgb: {
      active: false,
      red: 0,
      green: 0,
      blue: 0,
    },
    hsv: {
      active: false,
      saturation: 1.0,
      contrast: 1.0,
      brightness: 0,
    },
    dl: {
      active: false,
      conf: 0,
      iou: 0,
      max: 0,
      img: 160,
    },
  });

  useEffect(() => {
    socket = new WebSocket(`ws://${location.host}/ws`);

    /**
     * Handles the WebSocket connection being established.
     */
    socket.onopen = () => {
      console.log('WebSocket connection established.');
    };

    socket.addEventListener('message', handleSocketMessage);

    return () => {
      socket?.close();
    };
  }, []);

  /**
   * Handles input events from the user.
   */
  const handleInputEvent = (event: React.ChangeEvent) => {
    const element = event.target as HTMLInputElement;
    const key = element.id;
    const [tab, option] = element.id.split('/');

    let value: string | boolean | number | null = null;
    let settableValue: boolean | number | null = null;

    if (element.type === 'range') {
      value = element.value;
      settableValue = Number(value);
    } else if (element.type === 'checkbox') {
      value = element.checked;
      settableValue = value;
    } else if (element.type === 'select-one') {
      value = element.value;
    }

    sendMessage(key, value?.toString() || '');
    setOptions((prevOptions) => ({
      ...prevOptions,
      [tab]: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ...(prevOptions as any)[tab],
        [option]: settableValue,
      },
    }));
  };

  /**
   * Handles messages received from the server.
   */
  const handleSocketMessage = (event: MessageEvent) => {
    const receivedMessage = event.data;
    const [key, receivedValue] = receivedMessage.split(': ');
    const value = receivedValue.toLowerCase();

    const [tab, option] = key.split('/');

    let settableValue: boolean | number | null = null;

    // attempt to convert value into a boolean or number
    if (value === 'true' || value === 'false') {
      settableValue = value === 'true';
    } else if (!Number.isNaN(Number(value))) {
      settableValue = Number(value);
    }

    setOptions((prevOptions) => ({
      ...prevOptions,
      [tab]: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ...(prevOptions as any)[tab],
        [option]: settableValue,
      },
    }));
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
                <ConfigOption value="default" name="Default" />
                { configOptions.map((option) => (
                  <ConfigOption key={option} name={option} />
                ))}
              </select>
            </div>
            <ConfigButton handleClick={reset} text="Reset" />
            <ConfigButton handleClick={save} text="Save" />
          </div>
          <div className="tabs">
            <TabLink name="RGB" currentTab={currentTab} setCurrentTab={setCurrentTab} />
            <TabLink name="HSV" currentTab={currentTab} setCurrentTab={setCurrentTab} />
            <TabLink name="Yolov8" currentTab={currentTab} setCurrentTab={setCurrentTab} />
          </div>
          <div className="tab-contents">
            { currentTab === 'RGB' && (
              <RgbTab options={options.rgb} handleChange={handleInputEvent} />
            )}
            { currentTab === 'HSV' && (
              <HsvTab options={options.hsv} handleChange={handleInputEvent} />
            )}
            { currentTab === 'Yolov8' && (
              <Yolov8Tab options={options.dl} handleChange={handleInputEvent} />
            )}
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
