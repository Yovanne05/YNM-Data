import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../../models/analysis/analysis.model';
import { ViewingTrend } from '../../models/analysis/temporal.stats.ts/viewving.trend.model';
import { API_CONFIG } from '../../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class TemporalAnalysisService {
  private apiUrl = `${API_CONFIG.API_URL}/temporal-analysis`;

  constructor(private http: HttpClient) { }

  getViewingTrends(period: 'day' | 'month' | 'year' = 'year'): Observable<ApiResponse<ViewingTrend[]>> {
    return this.http.get<ApiResponse<ViewingTrend[]>>(
      `${this.apiUrl}/viewing-trends?period=${period}`
    );
  }
}
