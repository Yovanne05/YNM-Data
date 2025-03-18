import { Injectable } from '@angular/core';
import { UtilisateurService } from './utilisateur.service';
import { Utilisateur } from '../models/utilisateur';
import { SerieService } from './serie.service';
import { Serie } from '../models/serie';

interface ServiceWithModel {
  service: any;
  model: any;
}

@Injectable({
  providedIn: 'root',
})
export class ServiceFactory {

  constructor(
    private utilisateurService: UtilisateurService,
    private serieService: SerieService
  ) {}

  getServiceAndModel(tableName: string): ServiceWithModel | null {
    switch (tableName) {
      case 'Utilisateur':
        return { service: this.utilisateurService, model: <Utilisateur> };
      case 'Serie':
        return { service: this.serieService, model: Serie };
      default:
        return null;
    }
  }
}
