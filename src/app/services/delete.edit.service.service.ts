import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/delete_edit'; // Remplacez par l'URL de votre API Python

  constructor(private http: HttpClient) {}

  // Supprimer un élément
  deleteItem(tableName: string, itemId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${tableName}/${itemId}`, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    });
  }

  // Modifier un élément
  updateItem(tableName: string, itemId: string, updatedData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${tableName}/${itemId}`, updatedData, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    });
  }
}