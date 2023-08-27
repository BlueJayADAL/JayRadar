import { HsvConfigOptions } from '../../types/HsvConfigOptions';

interface Props {
  options: HsvConfigOptions;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

/**
 * Tab for HSV settings.
 */
function HsvTab({ options, handleChange }: Props) {
  return (
    <div id="tab2" className="tab-content">
      <div>
        <input
          type="checkbox"
          id="hsv/active"
          name="hsv/active"
          checked={options.active}
          onChange={handleChange}
        />
        <label htmlFor="hsv/active">Active</label>
      </div>
      <div className="sliders">
        <div>
          <label htmlFor="hsv/saturation">Saturation:</label>
          <input
            type="range"
            id="hsv/saturation"
            name="hsv/saturation"
            min="0"
            max="10"
            step=".1"
            value={options.saturation}
            onChange={handleChange}
          />
          <span id="hsv/saturationValue">{options.saturation}</span>
        </div>
        <div>
          <label htmlFor="hsv/contrast">Contrast:</label>
          <input
            type="range"
            id="hsv/contrast"
            name="hsv/contrast"
            min="0"
            max="10"
            step=".1"
            value={options.contrast}
            onChange={handleChange}
          />
          <span id="hsv/contrastValue">{options.contrast}</span>
        </div>
        <div>
          <label htmlFor="hsv/brightness">Brightness:</label>
          <input
            type="range"
            id="hsv/brightness"
            name="hsv/brightness"
            min="-255"
            max="255"
            step="5"
            value={options.brightness}
            onChange={handleChange}
          />
          <span id="hsv/brightnessValue">{options.brightness}</span>
        </div>
      </div>
    </div>
  );
}

export default HsvTab;
