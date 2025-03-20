import { Injectable } from '@angular/core';
import { UtilisateurService } from './utilisateur.service';
import { AbonnementService } from './abonnement.service';
import { SerieService } from './serie.service';
import { StatutAbonnementFilter } from '../models/filter/utilisateur.filter';
import { FilterStrategy } from '../models/interface/filter.interface';

@Injectable({
  providedIn: 'root',
})
export class ServiceFactory {

  constructor(
    private utilisateurService: UtilisateurService,
    private abonnementService: AbonnementService,
    private serieService: SerieService
  ) {}

  getService(tableName: string): { service: any, filters: { [key: string]: FilterStrategy } } {

    switch (tableName) {
      case 'Utilisateur':
        return {
          service: this.utilisateurService,
          filters: {
            statutAbonnement: new StatutAbonnementFilter()
          }
        };
      
      case 'Abonnement':
        return {
          service: this.abonnementService,
          filters: {
            
          }
        };
      
      default:
        return {
          service: null,
          filters: {}
        };
    }
  }
}
