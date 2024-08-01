import { Yolov8ConfigOptions } from '../../types/Yolov8ConfigOptions';
import { HStack, Flex, Checkbox, Slider, SliderTrack, SliderFilledTrack, SliderThumb, Text } from '@chakra-ui/react';

interface Props {
  options: Yolov8ConfigOptions;
  handleChange: (value: string | number | boolean, event?: React.ChangeEvent | React.SyntheticEvent) => void;
}

/**
 * Tab for YoloV8 settings.
 */
function Yolov8Tab({ options, handleChange }: Props) {
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
        getAttribute: () => "dl/active", // Mimic getAttribute to return the slider's name
      },
    };
    handleChange(String(event.target.checked), syntheticEvent as unknown as React.SyntheticEvent);
  };
  return (
    <Flex direction="column" borderRadius="25px" justifyContent="center" alignItems="center" w="30vw" h="30vh" mb="2vw" bg="brand.dark_blue">
      <HStack spacing="5" w="70%">
        <Text color="white">YOLOv8</Text>
        <Checkbox color="brand.grey" isChecked={options.active} onChange={handleCheckboxChange}>
          Active
        </Checkbox>
      </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Conf:</Text>
          <Slider w="200px" min={0} max={1} step={0.01} value={options.conf} onChange={handleSliderChange("dl/conf")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.conf}</Text>
        </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">IOU:</Text>
          <Slider w="200px" min={0} max={1} step={0.01} value={options.iou} onChange={handleSliderChange("dl/iou")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.iou}</Text>
        </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Max:</Text>
          <Slider w="200px" min={0} max={100} step={1} value={options.max} onChange={handleSliderChange("dl/max")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.max}</Text>
        </HStack>
        <HStack spacing="5" w="70%">
          <Text color="brand.grey">Img:</Text>
          <Slider w="200px" min={160} max={640} step={32} value={options.img} onChange={handleSliderChange("dl/img")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text color="brand.grey">{options.img}</Text>
        </HStack>
    </Flex>
      );
    }

export default Yolov8Tab;
