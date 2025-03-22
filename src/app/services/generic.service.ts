import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_CONFIG } from '../config/api.config';
import { GenericTableInterface } from './interfaces/service.interface';
import { TablesResponse } from '../models/table_response';

@Injectable({
  providedIn: 'root',
})
export class GenericTableService implements GenericTableInterface {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) {}

  getTableData(tableName: string): Observable<Record<string, string>[]> {
    return this.http
      .get<Record<string, string>[]>(`${this.apiUrl}/${tableName}`)
      .pipe(
        catchError((err) => {
          console.error(
            `Erreur lors de la récupération des données de la table ${tableName}`,
            err
          );
          throw new Error(`Une erreur est survenue: ${err}`);
        })
      );
  }

  getTables(): Observable<TablesResponse> {
    return this.http.get<TablesResponse>(this.apiUrl + `/tables`).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des tables', err);
        throw new Error('Une erreur est survenue:', err);
      })
    );
  }

  getTableDataByTableName(table_name: string): Observable<TablesResponse> {
    return this.http
      .get<TablesResponse>(this.apiUrl + `/table/${table_name}`)
      .pipe(
        catchError((err) => {
          console.error(
            'Erreur lors de la récupération des données de la table',
            err
          );
          throw new Error('Une erreur est survenue:', err);
        })
      );
  }
}
