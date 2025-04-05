import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-viewing-trends-chart',
  standalone: true,
  imports: [],
  templateUrl: './viewing-trends-chart.component.html',
  styleUrl: './viewing-trends-chart.component.scss'
})
export class ViewingTrendsChartComponent implements OnChanges {
  @Input() viewingTrends: any[] = [];
  private chart: Chart | null = null;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['viewingTrends'] && this.viewingTrends) {
      this.renderChart();
    }
  }

  renderChart(): void {
    const ctx = document.getElementById('viewingTrendsChart') as HTMLCanvasElement;
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const periodMap = new Map<string, number>();
    this.viewingTrends.forEach(item => {
      const total = periodMap.get(item.period) || 0;
      periodMap.set(item.period, total + item.view_count);
    });

    const labels = Array.from(periodMap.keys());
    const data = Array.from(periodMap.values());

    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Visionnages par période',
          data: data,
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Tendances de visionnage'
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Nombre de visionnages'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Période'
            }
          }
        }
      }
    });
  }
}
