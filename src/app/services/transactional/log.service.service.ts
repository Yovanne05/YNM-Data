import { API_CONFIG } from '../../config/api.config';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LogService {
  private apiUrl = API_CONFIG.API_URL+"/logs/";

  constructor(private http: HttpClient) { }

  getLogs(): Observable<{ logs: [string, string][] }> {
    return this.http.get<{ logs: [string, string][] }>(this.apiUrl);
  }

  clearLogs(): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(this.apiUrl, {});
  }
}