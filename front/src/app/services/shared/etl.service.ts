import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../../config/api.config';

export interface ETLStatus {
  last_execution: string;
  status: 'completed' | 'running' | 'failed' | 'unknown';
  records_processed?: number;
}

@Injectable({
  providedIn: 'root'
})
export class EtlService {
  private apiUrl = `${API_CONFIG.API_URL}/etl`;

  constructor(private http: HttpClient) { }

  runETL(): Observable<any> {
    return this.http.post(`${this.apiUrl}/run`, {});
  }

  getETLStatus(): Observable<ETLStatus> {
    return this.http.get<ETLStatus>(`${this.apiUrl}/status`);
  }
}
