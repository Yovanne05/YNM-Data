import { Injectable } from '@angular/core';
import { ServiceInterface } from './service-interface';
import { Abonnement } from '../models/abonnement';
import { API_CONFIG } from '../config/api.config';
import { catchError, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AbonnementService implements ServiceInterface<Abonnement> {
  private apiUrl = API_CONFIG.API_URL + '/abonnement';

   constructor(private readonly http: HttpClient) { }

  getTableData(): Observable<Abonnement> {
    return this.http.get<Abonnement>(this.apiUrl).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des utilisateurs', err);
        throw new Error('Une erreur est survenue:', err);
      })
    );
  }
}
