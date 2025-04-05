import { Component, OnInit } from '@angular/core';
import { TopContentChartComponent } from '../../components/top-content-chart/top-content-chart.component';
import { ContentPerformanceChartComponent } from '../../components/content-performance-chart/content-performance-chart.component';
import { ViewingTrendsChartComponent } from '../../components/viewing-trends-chart/viewing-trends-chart.component';
import { DailyActivityChartComponent } from '../../components/daily-activity-chart/daily-activity-chart.component';
import { UserEngagementChartComponent } from '../../components/user-engagement-chart/user-engagement-chart.component';
import { ContentAnalysisService } from '../../../../services/analysis/content.analysis.service';
import { TemporalAnalysisService } from '../../../../services/analysis/temporal.analysis.service';
import { BehaviorAnalysisService } from '../../../../services/analysis/behavior.analysis.service';

@Component({
  selector: 'app-stats-dashboard',
  standalone: true,
  imports: [
    TopContentChartComponent,
    ContentPerformanceChartComponent,
    ViewingTrendsChartComponent,
    DailyActivityChartComponent,
    UserEngagementChartComponent
  ],
  templateUrl: './analysis-card.component.html',
  styleUrl: './analysis-card.component.scss'
})
export class AnalysisCardComponent implements OnInit {
  contentPerformance: any[] = [];
  topContent: any[] = [];
  viewingTrends: any[] = [];
  userEngagement: any;
  dailyActivity: any[] = [];

  constructor(
    private contentAnalysisService: ContentAnalysisService,
    private temporalAnalysisService: TemporalAnalysisService,
    private behaviorAnalysisService: BehaviorAnalysisService
  ) {}

  ngOnInit(): void {
    this.loadContentPerformance();
    this.loadTopContent();
    this.loadViewingTrends();
    this.loadDailyActivity();
    this.loadUserEngagement();
  }

  loadUserEngagement(): void {
    this.behaviorAnalysisService.getUserEngagement().subscribe({
      next: (response) => {
        this.userEngagement = response.data;
      },
      error: (err) => console.error('Error loading user engagement', err)
    });
  }

  loadContentPerformance(): void {
    this.contentAnalysisService.getContentPerformance().subscribe({
      next: (response) => {
        this.contentPerformance = response.data || [];
      },
      error: (err) => console.error('Error loading content performance', err)
    });
  }

  loadTopContent(): void {
    this.contentAnalysisService.getTopContent(5).subscribe({
      next: (response) => {
        this.topContent = response.data || [];
      },
      error: (err) => console.error('Error loading top content', err)
    });
  }

  loadViewingTrends(): void {
    this.temporalAnalysisService.getViewingTrends('month').subscribe({
      next: (response) => {
        this.viewingTrends = response.data || [];
      },
      error: (err) => console.error('Error loading viewing trends', err)
    });
  }

  loadDailyActivity(): void {
    this.behaviorAnalysisService.getDailyViewingActivity().subscribe({
      next: (response) => {
        this.dailyActivity = response.data?.by_date || [];
      },
      error: (err) => console.error('Error loading daily activity', err)
    });
  }
}
