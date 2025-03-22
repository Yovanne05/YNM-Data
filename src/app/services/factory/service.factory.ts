import { Injectable } from '@angular/core';
import { UtilisateurService } from '../utilisateur.service';
import { AbonnementService } from '../abonnement.service';

@Injectable({ providedIn: 'root' })
export class ServiceFactory {
  constructor(
    private utilisateurService: UtilisateurService,
    private abonnementService: AbonnementService
  ) {}

  getService(tableName: string): any {
    switch (tableName) {
      case 'utilisateur':
        return this.utilisateurService;
      case 'abonnement':
        return this.abonnementService;
      default:
        return null;
    }
  }
}
