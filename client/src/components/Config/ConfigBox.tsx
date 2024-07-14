import { Box, Flex, HStack, Select } from '@chakra-ui/react';
import ConfigOption from './ConfigOption';
import ConfigButton from './ConfigButton';

interface ConfigBoxProps {
    reset: () => void; // Assuming reset and save are functions without arguments
    save: () => void;
    configOptions: string[]; // Assuming configOptions is an array of strings
    configSelect: React.RefObject<HTMLSelectElement>; // Assuming configSelect is a ref to a select element
  }

function ConfigBox ({reset, save, configOptions, configSelect}:ConfigBoxProps) {
  return (
    <Flex borderRadius="25px" direction="column" alignItems="center" justifyContent="center" m="2vw" p="2vw" bg="brand.dark_blue">
        <Box>
        <Select id="none/config" ref={configSelect} mb="5" bg="brand.mid_blue" variant="Filled" color="white">
            <ConfigOption value="default" name="Default" />
            { configOptions.map((option) => (
                <ConfigOption key={option} name={option} />
            ))}
            </Select>
        </Box>
        <HStack spacing="8">
            <ConfigButton handleClick={reset} text="Reset" />
            <ConfigButton handleClick={save} text="Save" />
        </HStack>
    </Flex>
  );
}

export default ConfigBox;