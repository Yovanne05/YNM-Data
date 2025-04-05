import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../../models/analysis/analysis.model';
import { UserEngagement } from '../../models/analysis/comportement/user.engagement';
import { DailyViewingActivity } from '../../models/analysis/comportement/daily.activity.model';
import { API_CONFIG } from '../../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class BehaviorAnalysisService {
  private apiUrl = `${API_CONFIG.API_URL}/behavior-analysis`;

  constructor(private http: HttpClient) { }

  getUserEngagement(): Observable<ApiResponse<UserEngagement>> {
    return this.http.get<ApiResponse<UserEngagement>>(
      `${this.apiUrl}/engagement`
    );
  }

  getDailyViewingActivity(): Observable<ApiResponse<DailyViewingActivity>> {
    return this.http.get<ApiResponse<DailyViewingActivity>>(
      `${this.apiUrl}/viewing-activity`
    );
  }
}
