import { Yolov8ConfigOptions } from '../../types/Yolov8ConfigOptions';

interface Props {
  options: Yolov8ConfigOptions;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

/**
 * Tab for YoloV8 settings.
 */
function Yolov8Tab({ options, handleChange }: Props) {
  return (
    <div id="tab3" className="tab-content">
      <div className="neural_checkboxes">
        <div>
          <input
            type="checkbox"
            id="dl/active"
            name="dl/active"
            checked={options.active}
            onChange={handleChange}
          />
          <label htmlFor="dl/active">Active</label>
        </div>
      </div>
      <div className="sliders">
        <div>
          <label htmlFor="dl/conf">Conf:</label>
          <input
            type="range"
            id="dl/conf"
            name="dl/conf"
            min="0"
            max="1"
            step=".01"
            value={options.conf}
            onChange={handleChange}
          />
          <span id="dl/confValue">{options.conf}</span>
        </div>
        <div>
          <label htmlFor="dl/iou">IOU:</label>
          <input
            type="range"
            id="dl/iou"
            name="dl/iou"
            min="0"
            max="1"
            step=".01"
            value={options.iou}
            onChange={handleChange}
          />
          <span id="dl/iouValue">{options.iou}</span>
        </div>
        <div>
          <label htmlFor="dl/max">Max:</label>
          <input
            type="range"
            id="dl/max"
            name="dl/max"
            min="0"
            max="100"
            step="1"
            value={options.max}
            onChange={handleChange}
          />
          <span id="dl/maxValue">{options.max}</span>
        </div>
        <div>
          <label htmlFor="dl/img">Img:</label>
          <input
            type="range"
            id="dl/img"
            name="dl/img"
            min="160"
            max="640"
            step="32"
            value={options.img}
            onChange={handleChange}
          />
          <span id="dl/imgValue">{options.img}</span>
        </div>
      </div>
    </div>
  );
}

export default Yolov8Tab;
