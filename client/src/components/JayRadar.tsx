/* eslint-disable no-restricted-globals */
import { useEffect, useRef, useState } from 'react';
import RgbTab from './Tabs/RgbTab';
import HsvTab from './Tabs/HsvTab';
import Yolov8Tab from './Tabs/Yolov8Tab';
import { TabOptions } from '../types/TabOptions';
import { Image, Flex, Box, Heading } from '@chakra-ui/react';
import ConfigBox from './Config/ConfigBox';
import logo from '../../public/logo.png';

// FYI - this is a temporary component that will be removed later.
// this will be used while we build and improve the rest of the UI.

let socket: WebSocket | null = null;

/**
 * Temporary component that renders the entire UI.
 */
function JayRadar() {
  const configSelect = useRef<HTMLSelectElement>(null);
  const configOptions = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

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
  const handleInputEvent = (value: string | number | boolean, event?: React.ChangeEvent | React.SyntheticEvent) => {
    // Use a custom attribute (e.g., data-id) to store the id
    const element = event?.target as HTMLElement;
    const key = element.getAttribute('data-id');
    if (!key) return;
  
    const [tab, option] = key.split('/');
  
    let settableValue: boolean | number | null = null;
  
    if (typeof value === 'boolean') {
      settableValue = value;
    } else if (typeof value === 'number') {
      settableValue = value;
    } else {
      // Handle other types as needed
    }
  
    sendMessage(key, value.toString());
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
  <Flex>
    <Flex direction="column" alignItems="center" w="150px" h="100vh" bg="brand.dark_blue">
      <Image src={logo} pt="25px" boxSize="100px"/>
      <Heading as="u" color="brand.light_blue" size="md" pt="25px">Tuning</Heading>
      <Heading color="white" size="md" pt="25px">Settings</Heading>
    </Flex>
    <Flex w="calc(100vw - 150px)" h="100vh" alignItems="center" justifyContent="center" bg="brand.background">
      <Box>
        <ConfigBox reset={reset} save={save} configOptions={configOptions} configSelect={configSelect}/> 
        <Image id="videoFeed" src="video_feed" alt="video feed" boxSize="65vh" bg="brand.dark_blue" p="10px" borderRadius="25px" />
      
      </Box>


      <Box ml="5vw">
        <RgbTab options={options.rgb} handleChange={handleInputEvent} />
        <HsvTab options={options.hsv} handleChange={handleInputEvent} />
        <Yolov8Tab options={options.dl} handleChange={handleInputEvent} />
      </Box>
      
    </Flex>
  </Flex> 
  );
}

export default JayRadar;
