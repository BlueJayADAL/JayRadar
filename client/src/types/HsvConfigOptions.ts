import { BaseConfigOptions } from './BaseConfigOptions';

export interface HsvConfigOptions extends BaseConfigOptions {
  active: boolean;
  saturation: number;
  contrast: number;
  brightness: number;
}
