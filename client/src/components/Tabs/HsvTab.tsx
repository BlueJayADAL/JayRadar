import { HsvConfigOptions } from '../../types/HsvConfigOptions';
import { Box, HStack, Flex, Checkbox, Slider, SliderTrack, SliderThumb, SliderFilledTrack, Text } from '@chakra-ui/react';

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
    <Flex direction="column" borderRadius="25px" justifyContent="center" alignItems="center" w="30vw" h="20vh" mb="2vw" bg="brand.dark_blue">
      <Checkbox color="brand.grey" isChecked={options.active} onChange={handleCheckboxChange} name="hsv/active">
        Active
      </Checkbox>
      <Box className="sliders">
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Saturation:</Text>
          <Slider w="300px" min={0} max={10} step={0.01} value={options.saturation} onChange={handleSliderChange("hsv/saturation")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.saturation}</Text>
        </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Contrast:</Text>
          <Slider w="300px" min={0} max={10} step={0.01} value={options.contrast} onChange={handleSliderChange("hsv/contrast")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.contrast}</Text>
        </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Brightness:</Text>
          <Slider w="300px" min={-255} max={255} step={5} value={options.brightness} onChange={handleSliderChange("hsv/brightness")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.brightness}</Text>
        </HStack>
      </Box>
    </Flex>
  );
}

export default HsvTab;
