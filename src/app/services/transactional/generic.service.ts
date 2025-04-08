import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,HttpErrorResponse } from '@angular/common/http';
import { Observable,throwError, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_CONFIG } from '../../config/api.config';
import { TableStructure } from '../../models/transactionnal/table_response';

@Injectable({
  providedIn: 'root',
})
export class GenericTableService {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) {}

  getTableData(
  tableName: string,
  filters?: { [key: string]: { operator: string, value: string } }
): Observable<Record<string, string>[]> {
  let params = new HttpParams();

  if (filters) {
    Object.keys(filters).forEach(key => {
      const filter = filters[key];
      if (filter.value) {
        params = params.set(`${key}__${filter.operator}`, filter.value);
      }
    });
  }

  return this.http.get<Record<string, string>[]>(
    `${this.apiUrl}/${tableName}`,
    { params }
  ).pipe(
    catchError((err) => {
      console.error(
        `Erreur lors de la récupération des données de la table ${tableName}`,
        err
      );
      throw new Error(`Une erreur est survenue: ${err}`);
    })
  );
}

  getTables(): Observable<TableStructure> {
    return this.http.get<TableStructure>(`${this.apiUrl}/tables`).pipe(
      catchError((err) => {
        console.error('Erreur lors de la récupération des tables', err);
        throw new Error(`Une erreur est survenue: ${err}`);
      })
    );
  }

  getTableDataByTableName(table_name: string): Observable<TableStructure> {
    return this.http
      .get<TableStructure>(`${this.apiUrl}/${table_name}/structure`)
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
    const id = this.extractIdFromItem(tableName, item);
    const requestBody = {
      table: tableName,
      item: item,
    };

    return this.http
      .delete(`${this.apiUrl}/${tableName}/${id}`, {
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

  createItem(tableName: string, data: any): Observable<{id: number}> {
    return this.http.post<{id: number}>(`${this.apiUrl}/${tableName}`, data).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error('Full error:', {
          url: error.url,
          status: error.status,
          serverMessage: error.error?.error || error.error,
          validationErrors: error.error?.missing_fields || error.error?.errors
        });
  
        let userMessage = 'Erreur lors de la création';
        if (error.status === 400) {
          if (error.error?.missing_fields) {
            userMessage = `Champs manquants: ${error.error.missing_fields.join(', ')}`;
          } else if (error.error?.error) {
            userMessage = error.error.error;
          }
        }
  
        return throwError(() => new Error(userMessage));
      })
    );
  }

  updateItem(tableName: string, item: any, updatedData: any): Observable<any> {
    const id = this.extractIdFromItem(tableName, item);

    return this.http
      .put(`${this.apiUrl}/${tableName}/${id}`, updatedData, {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
      })
      .pipe(
        catchError((err) => {
          console.error('Erreur détaillée:', err.error);
          throw err;
        })
      );
  }


  getTableSchema(tableName: string): Observable<{[key: string]: string}> {
    return this.http.get<{[key: string]: string}>(
      `${this.apiUrl}/${tableName}/schema`
    ).pipe(
      catchError(err => {
        console.error('Error fetching schema', err);
        return of({});
      })
    );
  }

  private extractIdFromItem(tableName: string, item: any): number {
    const pascalCaseTable =
      tableName.charAt(0).toUpperCase() + tableName.slice(1);
    const idColumn = `id${pascalCaseTable}`;

    const idKey = Object.keys(item).find((key) =>
      key.toLowerCase().startsWith('id')
    );

    const idValue =
      item[idColumn] || (idKey ? item[idKey] : undefined) || item['id'];

    if (!idValue) {
      throw new Error(
        `Aucun ID détecté pour ${tableName}. ` +
          `Colonnes disponibles: ${Object.keys(item).join(', ')}`
      );
    }

    const numericId = Number(idValue)
    return numericId;
  }

}
