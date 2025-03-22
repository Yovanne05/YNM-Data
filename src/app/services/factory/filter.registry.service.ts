import { Injectable } from '@angular/core';
import { FilterStrategy } from '../../models/interface/filter.interface';
import { StatutAbonnementFilter } from '../../models/filter/utilisateur.filter';

@Injectable({ providedIn: 'root' })
export class FilterRegistryService {
  private filters: { [key: string]: { strategy: FilterStrategy; name: string } } = {};

  constructor() {
    this.registerDefaultFilters();
  }

  private registerDefaultFilters(): void {
    this.registerFilter('statutAbonnement', new StatutAbonnementFilter(), 'Statut Abonnement');
  }

  registerFilter(key: string, filter: FilterStrategy, name: string): void {
    this.filters[key] = { strategy: filter, name };
  }

  getFilter(key: string): FilterStrategy | undefined {
    return this.filters[key]?.strategy;
  }

  getFilterName(key: string): string | undefined {
    return this.filters[key]?.name;
  }

  getFiltersForTable(tableName: string): { [key: string]: string } {
    const filters: { [key: string]: string } = {};

    switch (tableName) {
      case 'utilisateur':
        filters['statutAbonnement'] = this.getFilterName('statutAbonnement') || 'Statut Abonnement';
        break;
    }
    return filters;
  }
}
