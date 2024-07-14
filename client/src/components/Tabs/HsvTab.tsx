import { HsvConfigOptions } from '../../types/HsvConfigOptions';
import { Box, Flex, Checkbox, Slider, SliderTrack, SliderThumb, SliderFilledTrack, Text } from '@chakra-ui/react';

interface Props {
  options: HsvConfigOptions;
  handleChange: (value: string | number | boolean, event?: React.ChangeEvent | React.SyntheticEvent) => void;
}

/**
 * Tab for HSV settings.
 */
function HsvTab({ options, handleChange }: Props) {
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
        getAttribute: () => "hsv/active", // Mimic getAttribute to return the slider's name
      },
    };
    handleChange(String(event.target.checked), syntheticEvent as unknown as React.SyntheticEvent);
  };
  return (
    <Box>
      
      <Checkbox isChecked={options.active} onChange={handleCheckboxChange} id="hsv/active" name="hsv/active">
        Active
      </Checkbox>
      <Box className="sliders">
        <Flex>
          <Text>Saturation:</Text>
          <Slider min={0} max={10} step={0.1} value={options.saturation} onChange={handleSliderChange("hsv/saturation")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text >{options.saturation}</Text>
        </Flex>
        <Flex>
          <Text>Contrast:</Text>
          <Slider min={0} max={10} step={0.1} value={options.contrast} onChange={handleSliderChange("hsv/contrast")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.contrast}</Text>
        </Flex>
        <Flex>
          <Text>Brightness:</Text>
          <Slider min={-255} max={255} step={5} value={options.brightness} onChange={handleSliderChange("hsv/brightness")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.brightness}</Text>
        </Flex>
      </Box>
    </Box>
  );
}

export default HsvTab;
