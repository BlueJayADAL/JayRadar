import { Flex, HStack, Text, Checkbox, Slider, SliderTrack, SliderFilledTrack, SliderThumb } from '@chakra-ui/react';
import { RgbConfigOptions } from '../../types/RgbConfigOptions';

interface Props {
  options: RgbConfigOptions;
  handleChange: (value: string | number | boolean, event?: React.ChangeEvent | React.SyntheticEvent) => void;
}

function RgbTab({ options, handleChange }: Props) {
  // Adjusted handleSliderChange to create a synthetic event with the required data-id attribute
  const handleSliderChange = (name: string) => (value: number) => {
    const syntheticEvent = {
      target: {
        getAttribute: () => name, // Mimic getAttribute to return the slider's name
      },
    };
    handleChange(value, syntheticEvent as unknown as React.SyntheticEvent); // Cast to match expected type
  };

  // Adjusted handleCheckboxChange to directly pass the event
  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const syntheticEvent = {
      target: {
        getAttribute: () => "rgb/active", // Mimic getAttribute to return the slider's name
      },
    };
    handleChange(String(event.target.checked), syntheticEvent as unknown as React.SyntheticEvent);
  };

  return (
    <Flex direction="column" borderRadius="25px" justifyContent="center" alignItems="center" w="30vw" h="30vh" mb="2vw" bg="brand.dark_blue">
      <Checkbox isChecked={options.active} onChange={handleCheckboxChange} color="brand.grey">
        Active
      </Checkbox>
      <HStack spacing="5" w="70%">
        <Text color="brand.grey">Red Balance:</Text>
        <Slider 
          w="300px" 
          min={-255}
          max={255}
          step={5}
          value={options.red}
          onChange={handleSliderChange("rgb/red")}
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
        <Text color="brand.grey">{options.red}</Text>
      </HStack>
      <HStack spacing="5" w="70%">
        <Text color="brand.grey">Green Balance:</Text>
        <Slider 
          w="300px" 
          min={-255}
          max={255}
          step={5}
          value={options.green}
          onChange={handleSliderChange("rgb/green")}
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
        <Text color="brand.grey">{options.green}</Text>
      </HStack>
      <HStack spacing="5" w="70%">
        <Text color="brand.grey">Blue Balance:</Text>
        <Slider 
          w="300px" 
          min={-255}
          max={255}
          step={5}
          value={options.blue}
          onChange={handleSliderChange("rgb/blue")}
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
        <Text color="brand.grey">{options.blue}</Text>
      </HStack>
    </Flex>
  );
}

export default RgbTab;
