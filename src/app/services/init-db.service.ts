import { Injectable } from '@angular/core';
import { API_CONFIG } from '../config/api.config';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InitDbService {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) {}

  reset_db(): Observable<any> {
    return this.http.post<any>(this.apiUrl + '/initialise', '', {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    });
  }
}
