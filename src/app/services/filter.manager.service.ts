import { Injectable } from '@angular/core';
import { FilterRegistryService } from './filter.registry.service';

@Injectable({ providedIn: 'root' })
export class FilterManagerService {
  constructor(private filterRegistry: FilterRegistryService) {}

  applyFilters(data: Record<string, string>[], activeFilters: { [key: string]: boolean }): Record<string, string>[] {
    let filteredData = data;

    Object.keys(activeFilters).forEach(filterKey => {
      if (activeFilters[filterKey]) {
        const filter = this.filterRegistry.getFilter(filterKey);
        if (filter) {
          filteredData = filter.filter(filteredData);
        }
      }
    });

    return filteredData;
  }
}
