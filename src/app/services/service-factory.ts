import { Injectable } from '@angular/core';
import { UtilisateurService } from './utilisateur.service';
import { Utilisateur } from '../models/utilisateur';

@Injectable({
  providedIn: 'root',
})
export class ServiceFactory {

  constructor(
    private utilisateurService: UtilisateurService
  ) {}

  getService(tableName: string) {
    switch (tableName) {
      case 'Utilisateur':
        return this.utilisateurService;
    }
  }

  getModel(tableName: string){
    switch(tableName){
        case 'Utilisateur':
            return 
    }
  }
}
