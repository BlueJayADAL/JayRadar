interface Props {
  handleClick: () => void;
  text: string;
}

/**
 * A basic button component used for resetting / saving configs
 */
function ConfigButton({ handleClick, text }: Props) {
  return (
    <button onClick={handleClick} type="button">
      {text}
    </button>
  );
}

export default ConfigButton;
