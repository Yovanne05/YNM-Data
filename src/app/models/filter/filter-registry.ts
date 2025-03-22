import { Injectable } from "@angular/core";
import { FilterStrategy } from "../interface/filter.interface";

@Injectable({ providedIn: 'root' })

export class FilterRegistry {
  private filters: { [key: string]: { strategy: FilterStrategy, metadata: any } } = {};

  registerFilter(key: string, strategy: FilterStrategy, metadata: any): void {
    this.filters[key] = { strategy, metadata };
  }

  getFilter(key: string): { strategy: FilterStrategy, metadata: any } | undefined {
    return this.filters[key];
  }

  getFilters(): { [key: string]: { strategy: FilterStrategy, metadata: any } } {
    return this.filters;
  }
}
