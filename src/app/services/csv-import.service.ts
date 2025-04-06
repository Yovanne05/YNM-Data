import { Injectable } from '@angular/core';
import { API_CONFIG } from '../config/api.config';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsvImportService {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) {}

  sendCSVData(file: File, tableName: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tableName', tableName);
    return this.http.post<any>(this.apiUrl + '/import_data', formData);
  }
}
