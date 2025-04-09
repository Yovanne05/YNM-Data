import { Component, OnInit, OnDestroy } from '@angular/core';
import { TopContentChartComponent } from '../../components/top-content-chart/top-content-chart.component';
import { ContentPerformanceChartComponent } from '../../components/content-performance-chart/content-performance-chart.component';
import { ViewingTrendsChartComponent } from '../../components/viewing-trends-chart/viewing-trends-chart.component';
import { DailyActivityChartComponent } from '../../components/daily-activity-chart/daily-activity-chart.component';
import { UserEngagementChartComponent } from '../../components/user-engagement-chart/user-engagement-chart.component';
import { BehaviorAnalysisService } from '../../../../services/analysis/behavior.analysis.service';
import { ContentAnalysisService } from '../../../../services/analysis/content.analysis.service';
import { TemporalAnalysisService } from '../../../../services/analysis/temporal.analysis.service';
import { EtlService } from '../../../../services/shared/etl.service';
import { Subscription, forkJoin } from 'rxjs';
import { DailyViewingActivity } from '../../../../models/analysis/comportement/daily.activity.model';
import { UserEngagement } from '../../../../models/analysis/comportement/user.engagement';
import { ContentPerformance } from '../../../../models/analysis/content/content.perf.model';
import { TopContent } from '../../../../models/analysis/content/top.content.model';
import { ViewingTrend } from '../../../../models/analysis/temporal.stats.ts/viewving.trend.model';

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
  templateUrl: './analysis-page.component.html',
  styleUrl: './analysis-page.component.scss'
})
export class AnalysisPageComponent implements OnInit, OnDestroy {
  dailyActivity: DailyViewingActivity['by_date'] = [];
  userEngagement?: UserEngagement;
  contentPerformance: ContentPerformance[] = [];
  topContent: TopContent[] = [];
  viewingTrends: ViewingTrend[] = [];

  isEtlRunning = false;
  etlMessage = '';
  showEtlMessage = false;
  isEtlError = false;
  private subscriptions = new Subscription();

  constructor(
    private behaviorAnalysisService: BehaviorAnalysisService,
    private contentAnalysisService: ContentAnalysisService,
    private temporalAnalysisService: TemporalAnalysisService,
    private etlService: EtlService,
  ) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  runETLProcess(): void {
    this.isEtlRunning = true;
    this.showEtlMessage = false;

    const etlSub = this.etlService.runETL().subscribe({
      next: (response) => {
        this.showEtlNotification('ETL process completed successfully!', false);
        this.loadAllData();
      },
      error: (err) => {
        this.showEtlNotification(`ETL process failed: ${err.error?.message || 'Unknown error'}`, true);
      },
      complete: () => {
        this.isEtlRunning = false;
      }
    });
    this.subscriptions.add(etlSub);
  }

  private loadAllData(): void {
    forkJoin([
      this.behaviorAnalysisService.getUserEngagement(),
      this.behaviorAnalysisService.getDailyViewingActivity(),
      this.contentAnalysisService.getTopContent(5),
      this.contentAnalysisService.getContentPerformance(),
      this.temporalAnalysisService.getViewingTrends('day')
    ]).subscribe({
      next: ([
        userEngagementRes,
        dailyActivityRes,
        topContentRes,
        contentPerformanceRes,
        viewingTrendsRes
      ]) => {
        if (userEngagementRes.success) this.userEngagement = userEngagementRes.data;
        if (dailyActivityRes.success) this.dailyActivity = dailyActivityRes.data?.by_date || [];
        if (topContentRes.success) this.topContent = topContentRes.data || [];
        if (contentPerformanceRes.success) this.contentPerformance = contentPerformanceRes.data || [];
        if (viewingTrendsRes.success) this.viewingTrends = viewingTrendsRes.data || [];
      },
      error: (err) => {
        console.error('Error loading dashboard data', err);
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
}
