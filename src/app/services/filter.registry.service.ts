import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class FilterRegistryService {
  private filters: { [key: string]: string } = {}; //key = cle json python, string = nom titre

  constructor() {
    this.registerDefaultFilters();
  }

  private registerDefaultFilters(): void {
    this.registerFilter('statutAbonnement', 'Statut Abonnement');
    this.registerFilter('age', 'Utilisateur Majeur');
    this.registerFilter('paysResidence', 'Pays de résidence');
    this.registerFilter('prix', 'Prix');
  }

  registerFilter(key: string, name: string): void {
    this.filters[key] = name;
  }

  getFilterName(key: string): string {
    return this.filters[key] || '';
  }

  getFiltersForTable(tableName: string): { [key: string]: string } {
    const filtersChoose: { [key: string]: string } = {};

    switch (tableName) {
      case 'utilisateur':
        filtersChoose['statutAbonnement'] = this.getFilterName('statutAbonnement');
        filtersChoose['age'] = this.getFilterName('age');
        break;
      case 'abonnement':
        filtersChoose['prix'] = this.getFilterName("prix");
    }
    return filtersChoose;
  }
}
