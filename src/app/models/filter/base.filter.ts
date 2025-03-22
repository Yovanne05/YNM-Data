import { FilterStrategy } from "../interface/filter.interface";

export abstract class BaseFilter implements FilterStrategy {
  abstract filter(data: Record<string, string>[]): Record<string, string>[];
}
