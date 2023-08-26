import { HsvConfigOptions } from './HsvConfigOptions';
import { RgbConfigOptions } from './RgbConfigOptions';
import { Yolov8ConfigOptions } from './Yolov8ConfigOptions';

export interface TabOptions {
  rgb: RgbConfigOptions;
  hsv: HsvConfigOptions;
  dl: Yolov8ConfigOptions;
}
