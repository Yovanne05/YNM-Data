import { Component, OnInit } from '@angular/core';
import { TopContentChartComponent } from '../../components/top-content-chart/top-content-chart.component';
import { ContentPerformanceChartComponent } from '../../components/content-performance-chart/content-performance-chart.component';
import { ViewingTrendsChartComponent } from '../../components/viewing-trends-chart/viewing-trends-chart.component';
import { DailyActivityChartComponent } from '../../components/daily-activity-chart/daily-activity-chart.component';
import { UserEngagementChartComponent } from '../../components/user-engagement-chart/user-engagement-chart.component';
import { ContentAnalysisService } from '../../../../services/analysis/content.analysis.service';
import { TemporalAnalysisService } from '../../../../services/analysis/temporal.analysis.service';
import { BehaviorAnalysisService } from '../../../../services/analysis/behavior.analysis.service';
import { EtlService } from '../../../../services/shared/etl.service';

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
  isEtlRunning = false;
  etlMessage = '';
  showEtlMessage = false;
  isEtlError = false;

  constructor(
    private contentAnalysisService: ContentAnalysisService,
    private temporalAnalysisService: TemporalAnalysisService,
    private behaviorAnalysisService: BehaviorAnalysisService,
    private etlService: EtlService
  ) {}

  ngOnInit(): void {
    this.loadContentPerformance();
    this.loadTopContent();
    this.loadViewingTrends();
    this.loadDailyActivity();
    this.loadUserEngagement();
  }

  runETLProcess(): void {
    this.isEtlRunning = true;
    this.showEtlMessage = false;

    this.etlService.runETL().subscribe({
      next: (response) => {
        this.showEtlNotification('ETL process completed successfully!', false);
        this.isEtlRunning = false;
        this.ngOnInit();
      },
      error: (err) => {
        this.showEtlNotification(`ETL process failed: ${err.error?.error || 'Unknown error'}`, true);
        this.isEtlRunning = false;
      }
    });
  }

  private showEtlNotification(message: string, isError: boolean): void {
    this.etlMessage = message;
    this.isEtlError = isError;
    this.showEtlMessage = true;

    setTimeout(() => {
      this.showEtlMessage = false;
    }, 5000);
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
