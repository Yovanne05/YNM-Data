import { Injectable } from '@angular/core';
import { AbonnementService } from './abonnement.service';
import { UtilisateurService } from './utilisateur.service';
import { StatutAbonnementFilter } from '../models/filter/utilisateur.filter';
import { FilterStrategy } from '../models/interface/filter.interface';

@Injectable({ providedIn: 'root' })
export class ServiceFactory {
  constructor(
    private utilisateurService: UtilisateurService,
    private abonnementService: AbonnementService,
  ) {}

  getService(tableName: string): {
    service: any,
    filters: { [key: string]: { strategy: FilterStrategy, name: string } }
  } {
    const filters: { [key: string]: { strategy: FilterStrategy, name: string } } = {};

    switch (tableName) {
      case 'utilisateur':
        filters['statutAbonnement'] = {
          strategy: new StatutAbonnementFilter(),
          name: 'Statut Abonnement'
        };
        return { service: this.utilisateurService, filters };

      case 'abonnement':
        return { service: this.abonnementService, filters : {} };

      default:
        return { service: null, filters: {} };
    }
  }
}
