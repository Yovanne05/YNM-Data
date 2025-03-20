import { Injectable } from '@angular/core';
import { ServiceInterface } from './interfaces/service.interface';
import { Abonnement } from '../models/abonnement';
import { API_CONFIG } from '../config/api.config';
import { catchError, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AbonnementService implements ServiceInterface{
  private apiUrl = API_CONFIG.API_URL + '/abonnement';

   constructor(private readonly http: HttpClient) { }

  getTableData(): Observable<Record<string, string>> {
    return this.http.get<Record<string, string>>(this.apiUrl).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des utilisateurs', err);
        throw new Error('Une erreur est survenue:', err);
      })
    );
  }
}
