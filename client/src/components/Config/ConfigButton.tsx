import { Button } from "@chakra-ui/react";

interface Props {
  handleClick: () => void;
  text: string;
}

/**
 * A basic button component used for resetting / saving configs
 */
function ConfigButton({ handleClick, text }: Props) {
  return (
    <Button onClick={handleClick} type="button" colorScheme="blue">
      {text}
    </Button>
  );
}

export default ConfigButton;
