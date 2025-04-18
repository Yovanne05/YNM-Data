import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,HttpErrorResponse } from '@angular/common/http';
import { Observable,throwError, of } from 'rxjs';
import { catchError,switchMap } from 'rxjs/operators';
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
    filters?: { [key: string]: { operator: string, value: string } },
    sortKeys?: { key: string; direction: 'asc' | 'desc' }[],
    page: number = 1,
    perPage: number = 15
  ): Observable<{items: Record<string, string>[], total: number, page: number, pages: number}> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());

    if (filters) {
      Object.keys(filters).forEach(key => {
        const filter = filters[key];
        if (filter.value) {
          params = params.set(`${key}__${filter.operator}`, filter.value);
        }
      });
    }

    if (sortKeys && sortKeys.length > 0) {
      sortKeys.forEach(sort => {
        params = params.set(`sort_${sort.key}`, sort.direction);
      });
    }

    return this.http.get<{items: any[], total: number, page: number, pages: number}>(
      `${this.apiUrl}/${tableName}/`,
      { params }
    ).pipe(
      catchError((err) => {
        console.error(`Erreur lors de la récupération des données`, err);
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
    return this.http.get<{is_composite: boolean, columns: string[]}>(
      `${this.apiUrl}/${tableName}/primary-keys`
    ).pipe(
      switchMap(pkInfo => {
            if (!pkInfo) throw new Error('Impossible de récupérer les informations de clé primaire');

            if (pkInfo.is_composite) {
                const compositeKey: Record<string, any> = {};

                pkInfo.columns.forEach((col: string) => {
                    if (item[col] === undefined || item[col] === null) {
                        throw new Error(`Item manque la colonne clé primaire: ${col}`);
                    }
                    compositeKey[col] = item[col];
                });

                return this.http.delete(`${this.apiUrl}/${tableName}`, {
                    body: compositeKey,
                    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
                });
            } else {
                const idColumn = pkInfo.columns[0];
                const id = item[idColumn] || item['id'];
                if (id === undefined || id === null) {
                    throw new Error('ID manquant pour la suppression');
                }
                return this.http.delete(`${this.apiUrl}/${tableName}/${id}`);
            }
        }),
        catchError(error => {
            console.error('Erreur lors de la suppression:', error);
            return throwError(error);
        })
    );
}

  createItem(tableName: string, data: any): Observable<{id: number}> {
    return this.http.post<{id: number}>(`${this.apiUrl}/${tableName}/`, data).pipe(
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

  getColumnSchema(tableName: string, columnName: string): Observable<any> {
    return this.http.get<any>(
      `${this.apiUrl}/${tableName}/schema/${columnName}`
    ).pipe(
      catchError(err => {
        console.error(`Error fetching schema for ${columnName}:`, err);
        return of({
          type: 'text',
          values: []
        });
      })
    );
  }

  getTableDataNoPagination(
    tableName: string,
    params: Record<string, string>
  ): Observable<Record<string, string>[]> {
    let httpParams = new HttpParams();

    Object.keys(params).forEach(key => {
      if (params[key]) {
        httpParams = httpParams.set(key, params[key]);
      }
    });

    return this.http.get<Record<string, string>[]>(
      `${this.apiUrl}/${tableName}/no_pagination`,
      { params: httpParams }
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

}
