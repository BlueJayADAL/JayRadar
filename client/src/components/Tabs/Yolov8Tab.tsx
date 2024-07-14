import { Yolov8ConfigOptions } from '../../types/Yolov8ConfigOptions';
import { Box, Flex, Checkbox, Slider, SliderTrack, SliderFilledTrack, SliderThumb, Text } from '@chakra-ui/react';

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
    <Box>
      <Checkbox id="dl/active" name="dl/active" isChecked={options.active} onChange={handleCheckboxChange}>
        Active
      </Checkbox>
      <Box className="sliders">
        <Flex>
          <Text>Conf:</Text>
          <Slider min={0} max={1} step={0.01} value={options.conf} onChange={handleSliderChange("dl/conf")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.conf}</Text>
        </Flex>
        <Flex>
          <Text>IOU:</Text>
          <Slider min={0} max={1} step={0.01} value={options.iou} onChange={handleSliderChange("dl/iou")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.iou}</Text>
        </Flex>
        <Flex>
          <Text>Max:</Text>
          <Slider min={0} max={100} step={1} value={options.max} onChange={handleSliderChange("dl/max")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.max}</Text>
        </Flex>
        <Flex>
          <Text>Img:</Text>
          <Slider min={160} max={640} step={32} value={options.img} onChange={handleSliderChange("dl/img")}>
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
          <Text>{options.img}</Text>
        </Flex>
      </Box>
    </Box>
      );
    }

export default Yolov8Tab;
