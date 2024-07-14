interface Props {
  name: string;
  value?: string;
}

/**
 * Config options used in the config selector component
 */
function ConfigOption({ name, value }: Props) {
  return (
    <option style={{ color: 'black' }} value={value ?? name}>
      Config:
      {' '}
      {name}
    </option>
  );
}

export default ConfigOption;
