import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { StatsService } from '../../../../services/analysis.service';
import { TopContentChartComponent } from '../../components/top-content-chart/top-content-chart.component';
import { ContentPerformanceChartComponent } from '../../components/content-performance-chart/content-performance-chart.component';
import { ViewingTrendsChartComponent } from '../../components/viewing-trends-chart/viewing-trends-chart.component';
import { DailyActivityChartComponent } from '../../components/daily-activity-chart/daily-activity-chart.component';
import { UserEngagementChartComponent } from '../../components/user-engagement-chart/user-engagement-chart.component';
import { Chart, registerables } from 'chart.js';


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

  currentSlide = 0;
  slides = [0, 1, 2, 3, 4];

  constructor(private statsService: StatsService) {}


  ngOnInit(): void {
    this.loadContentPerformance();
    this.loadTopContent();
    this.loadViewingTrends();
    this.loadDailyActivity();
    this.loadUserEngagement();
  }

  loadUserEngagement(): void {
    this.statsService.getUserEngagement().subscribe({
      next: (response) => {
        this.userEngagement = response.data;
      },
      error: (err) => console.error('Error loading user engagement', err)
    });

  }

  loadContentPerformance(): void {
    this.statsService.getContentPerformance().subscribe({
      next: (response) => {
        this.contentPerformance = response.data || [];
      },
      error: (err) => console.error('Error loading content performance', err)
    });

  }

  loadTopContent(): void {
    this.statsService.getTopContent(5).subscribe({
      next: (response) => {
        this.topContent = response.data || [];
      },
      error: (err) => console.error('Error loading top content', err)
    });

  }

  loadViewingTrends(): void {
    this.statsService.getViewingTrends('month').subscribe({
      next: (response) => {
        this.viewingTrends = response.data || [];
      },
      error: (err) => console.error('Error loading viewing trends', err)
    });
  }

  loadDailyActivity(): void {
    this.statsService.getDailyViewingActivity().subscribe({
      next: (response) => {
        this.dailyActivity = response.data?.by_date || [];
      },
      error: (err) => console.error('Error loading daily activity', err)
    });

  }

  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.slides.length;
  }

  prevSlide(): void {
    this.currentSlide = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
  }

  goToSlide(index: number): void {
    this.currentSlide = index;
  }
}
