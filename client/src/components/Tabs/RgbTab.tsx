import { RgbConfigOptions } from '../../types/RgbConfigOptions';

interface Props {
  options: RgbConfigOptions;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

/**
 * Tab for RGB settings.
 */
function RgbTab({ options, handleChange }: Props) {
  return (
    <div id="tab1" className="tab-content">
      <div>
        <input
          type="checkbox"
          id="rgb/active"
          name="rgb/active"
          checked={options.active}
          onChange={handleChange}
        />
        <label htmlFor="rgb/active">Active</label>
      </div>
      <div className="sliders">
        <div>
          <label htmlFor="rgb/red">Red Balance:</label>
          <input
            type="range"
            id="rgb/red"
            name="rgb/red"
            min="-255"
            max="255"
            step="5"
            value={options.red}
            onChange={handleChange}
          />
          <span id="rgb/redValue">{options.red}</span>
        </div>
        <div>
          <label htmlFor="rgb/green">Green Balance:</label>
          <input
            type="range"
            id="rgb/green"
            name="rgb/green"
            min="-255"
            max="255"
            step="5"
            value={options.green}
            onChange={handleChange}
          />
          <span id="rgb/greenValue">{options.green}</span>
        </div>
        <div>
          <label htmlFor="rgb/blue">Blue Balance:</label>
          <input
            type="range"
            id="rgb/blue"
            name="rgb/blue"
            min="-255"
            max="255"
            step="5"
            value={options.blue}
            onChange={handleChange}
          />
          <span id="rgb/blueValue">{options.blue}</span>
        </div>
      </div>
    </div>
  );
}

export default RgbTab;
