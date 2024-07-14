import { Box, Flex, Text, Checkbox, Slider, SliderTrack, SliderFilledTrack, SliderThumb } from '@chakra-ui/react';
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
    <Box>
      <Checkbox
        data-id="rgb/active" // Ensure data-id is set for handleInputEvent to work
        name="rgb/active"
        isChecked={options.active}
        onChange={handleCheckboxChange}
      >
        Active
      </Checkbox>
      <Flex>
        <Text as="label" htmlFor="rgb/red" color="white">Red Balance:</Text>
        <Slider
          data-id="rgb/red" // Ensure data-id is set for handleInputEvent to work
          name="rgb/red"
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
        <Text data-id="rgb/redValue" color="white">{options.red}</Text>
      </Flex>
      <Flex>
        <Text as="label" htmlFor="rgb/green" color="white">Green Balance:</Text>
        <Slider
          data-id="rgb/green" // Ensure data-id is set for handleInputEvent to work
          name="rgb/green"
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
        <Text data-id="rgb/greenValue" color="white">{options.green}</Text>
      </Flex>
      <Flex>
        <Text as="label" color="white" htmlFor="rgb/blue">Blue Balance:</Text>
        <Slider
          data-id="rgb/blue" // Ensure data-id is set for handleInputEvent to work
          name="rgb/blue"
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
        <Text color="white" data-id="rgb/blueValue">{options.blue}</Text>
      </Flex>
    </Box>
  );
}

export default RgbTab;
