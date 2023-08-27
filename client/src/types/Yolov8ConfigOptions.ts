import { BaseConfigOptions } from './BaseConfigOptions';

export interface Yolov8ConfigOptions extends BaseConfigOptions {
  active: boolean;
  conf: number;
  iou: number;
  max: number;
  img: number;
}
