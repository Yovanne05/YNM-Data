import { Injectable } from '@angular/core';
import { UtilisateurService } from './utilisateur.service';
import { Utilisateur } from '../models/utilisateur';
import { SerieService } from './serie.service';


@Injectable({
  providedIn: 'root',
})


export class ServiceFactory {

  constructor(
    private utilisateurService: UtilisateurService,
    private serieService: SerieService
  ) {}

  getService(tableName: string){

    switch (tableName) {
      case 'utilisateur':
        return this.utilisateurService
      case 'Serie':
        return this.utilisateurService;
      default:
        return null;
    }
  }
}
