import { BaseConfigOptions } from './BaseConfigOptions';

export interface Yolov8ConfigOptions extends BaseConfigOptions {
  active: boolean;
  ss: boolean;
  ssd: boolean;
  half: boolean;
  conf: number;
  iou: number;
  max: number;
  img: number;
}
