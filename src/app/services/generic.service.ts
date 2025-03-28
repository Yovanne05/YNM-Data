import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_CONFIG } from '../config/api.config';
import { GenericTableInterface } from './interfaces/service.interface';
import { TablesResponse } from '../models/table_response';
import { tab } from '@testing-library/user-event/dist/tab';

@Injectable({
  providedIn: 'root',
})
export class GenericTableService implements GenericTableInterface {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) {}

  getTableData(
    tableName: string,
    filters?: { [key: string]: string }
  ): Observable<Record<string, string>[]> {
    let params = new HttpParams();
    if (filters) {
      Object.keys(filters).forEach((key) => {
        params = params.append(key, filters[key]);
      });
    }

    return this.http
      .get<Record<string, string>[]>(`${this.apiUrl}/table/${tableName}/data`, {
        params,
      })
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
    return this.http.get<TablesResponse>(`${this.apiUrl}/tables`).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des tables', err);
        throw new Error(`Une erreur est survenue: ${err}`);
      })
    );
  }

  getTableDataByTableName(table_name: string): Observable<TablesResponse> {
    return this.http
      .get<TablesResponse>(`${this.apiUrl}/table/${table_name}`)
      .pipe(
        catchError((err) => {
          console.error(
            'Erreur lors de la récupération des données de la table',
            err
          );
          throw new Error(`Une erreur est survenue: ${err}`);
        })
      );
  }

  deleteItem(tableName: string, item: any): Observable<any> {
    const requestBody = {
      table: tableName,
      item: item,
    };

    return this.http
      .delete(`${this.apiUrl}/${tableName}`, {
        body: requestBody,
        headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
      })
      .pipe(
        catchError((err) => {
          console.error(
            `Erreur lors de la suppression de l'élément de la table ${tableName}`,
            err
          );
          throw new Error(`Une erreur est survenue: ${err}`);
        })
      );
  }

  updateItem(tableName: string, item: any, updatedData: any): Observable<any> {
    console.log(tableName)
    const requestBody = {
      table: tableName,
      currentItem: item,
      updatedData: updatedData,
    };

    return this.http
      .put(`${this.apiUrl}/${tableName}`, requestBody, {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
      })
      .pipe(
        catchError((err) => {
          console.error(
            `Erreur lors de la mise à jour de l'élément de la table ${tableName}`,
            err
          );
          throw new Error(`Une erreur est survenue: ${err}`);
        })
      );
  }
}
