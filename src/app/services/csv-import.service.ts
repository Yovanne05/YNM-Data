import { Injectable } from '@angular/core';
import { API_CONFIG } from '../config/api.config';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsvImportService {
  private apiUrl = API_CONFIG.API_URL;
  aaa: string = "oui";

  constructor(private http: HttpClient) {}

  sendCSVData(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    //TODO : envoyer le nom de la table dans le composant pour pouvoir ajouter correctement les données
    return this.http.post<any>(this.apiUrl + '/import_data', formData);
  }
}
