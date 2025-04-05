import { Directive, Input, OnChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Directive()
export abstract class ChartBaseComponent implements OnChanges {
  @Input() chartData: any[] = [];
  protected chart: Chart | null = null;
  protected abstract chartId: string;
  protected abstract chartType: 'bar' | 'line' | 'pie' | 'doughnut';
  protected abstract chartTitle: string;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(): void {
    this.renderChart();
  }

  protected renderChart(): void {
    const ctx = document.getElementById(this.chartId) as HTMLCanvasElement;
    if (!ctx || !this.chartData || this.chartData.length === 0) return;

    this.destroyExistingChart(ctx);

    const chartConfig = this.getChartConfig();
    this.chart = new Chart(ctx, chartConfig);
  }

  protected destroyExistingChart(ctx: HTMLCanvasElement): void {
    const existingChart = Chart.getChart(ctx);
    if (existingChart) {
      existingChart.destroy();
    }
  }

  protected abstract getChartConfig(): any;

  protected getDefaultOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: this.chartTitle,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Nombre de vues',
          },
        },
        x: {
          title: {
            display: true,
            text: 'Date',
          },
        },
      },
    };
  }
}
