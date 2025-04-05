import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../models/analysis/analysis.model';
import { ContentPerformance } from '../models/analysis/content/content.perf.model';
import { TopContent } from '../models/analysis/content/top.content.model';
import { ViewingTrend } from '../models/analysis/temporal.stats.ts/viewving.trend.model';
import { UserEngagement } from '../models/analysis/comportement/user.engagement';
import { DailyViewingActivity } from '../models/analysis/comportement/daily.activity.model';
import { API_CONFIG } from '../config/api.config';

@Injectable({
  providedIn: 'root'
})

export class StatsService {
  private apiUrl = API_CONFIG.API_URL;

  constructor(private http: HttpClient) { }

  // Analyse de performance des contenus
  getContentPerformance(dateDebut?: string, dateFin?: string): Observable<ApiResponse<ContentPerformance[]>> {
    let url = `${this.apiUrl}/content-analysis/performance`;
    if (dateDebut && dateFin) {
      url += `?date_debut=${dateDebut}&date_fin=${dateFin}`;
    }
    return this.http.get<ApiResponse<ContentPerformance[]>>(url);
  }

  // Top contenus
  getTopContent(topN: number = 10): Observable<ApiResponse<TopContent[]>> {
    return this.http.get<ApiResponse<TopContent[]>>(
      `${this.apiUrl}/content-analysis/top-content?top_n=${topN}`
    );
  }

  // Tendances de visionnage
  getViewingTrends(period: 'day' | 'month' | 'year' = 'year'): Observable<ApiResponse<ViewingTrend[]>> {
    return this.http.get<ApiResponse<ViewingTrend[]>>(
      `${this.apiUrl}/temporal-analysis/viewing-trends?period=${period}`
    );
  }

  // Engagement utilisateur
  getUserEngagement(): Observable<ApiResponse<UserEngagement>> {
    return this.http.get<ApiResponse<UserEngagement>>(
      `${this.apiUrl}/behavior-analysis/engagement`
    );
  }

  // Activité quotidienne
  getDailyViewingActivity(): Observable<ApiResponse<DailyViewingActivity>> {
    return this.http.get<ApiResponse<DailyViewingActivity>>(
      `${this.apiUrl}/behavior-analysis/viewing-activity`
    );
  }
}
