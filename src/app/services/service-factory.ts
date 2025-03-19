import { Injectable } from '@angular/core';
import { UtilisateurService } from './utilisateur.service';
import { Utilisateur } from '../models/utilisateur';
import { SerieService } from './serie.service';
import { AbonnementService } from './abonnement.service';
@Injectable({
  providedIn: 'root',
})

export class ServiceFactory {

  constructor(
    private utilisateurService: UtilisateurService,
    private abonnementService: AbonnementService,
    private serieService: SerieService
  ) {}

  getService(tableName: string){

    switch (tableName) {
      case 'utilisateur':
        return this.utilisateurService
      case 'abonnement':
        return this.abonnementService;
      default:
        return null;
    }
  }
}
