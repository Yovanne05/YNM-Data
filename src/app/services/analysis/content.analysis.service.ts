import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../../models/analysis/analysis.model';
import { ContentPerformance } from '../../models/analysis/content/content.perf.model';
import { TopContent } from '../../models/analysis/content/top.content.model';
import { API_CONFIG } from '../../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class ContentAnalysisService {
  private apiUrl = `${API_CONFIG.API_URL}/content-analysis`;

  constructor(private http: HttpClient) { }

  getContentPerformance(dateDebut?: string, dateFin?: string): Observable<ApiResponse<ContentPerformance[]>> {
    let url = `${this.apiUrl}/performance`;
    if (dateDebut && dateFin) {
      url += `?date_debut=${dateDebut}&date_fin=${dateFin}`;
    }
    return this.http.get<ApiResponse<ContentPerformance[]>>(url);
  }

  getTopContent(topN: number = 10): Observable<ApiResponse<TopContent[]>> {
    return this.http.get<ApiResponse<TopContent[]>>(
      `${this.apiUrl}/top-content?top_n=${topN}`
    );
  }
}
