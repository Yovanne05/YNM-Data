import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable } from 'rxjs';
import { API_CONFIG } from '../config/api.config';
import { TablesResponse } from '../models/table_response';

@Injectable({
  providedIn: 'root',
})

export class DatabaseService {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private readonly http: HttpClient) {}

  getTables(): Observable<TablesResponse> {
    return this.http.get<TablesResponse>(this.apiUrl + `/tables`).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des tables', err);
        throw new Error('Une erreur est survenue:', err);
      })
    );
  }
}
