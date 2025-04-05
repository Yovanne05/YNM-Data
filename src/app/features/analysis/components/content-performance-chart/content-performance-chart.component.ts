import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-content-performance-chart',
  standalone: true,
  imports: [],
  templateUrl: './content-performance-chart.component.html',
  styleUrl: './content-performance-chart.component.scss'
})
export class ContentPerformanceChartComponent implements OnChanges {
  @Input() contentPerformance: any[] = [];
  private chart: Chart | null = null;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['contentPerformance'] && this.contentPerformance) {
      this.renderChart();
    }
  }

  renderChart(): void {
    const ctx = document.getElementById('contentPerformanceChart') as HTMLCanvasElement;
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const labels = this.contentPerformance.map(item => item.content_title);
    const data = this.contentPerformance.map(item => item.view_count);

    this.chart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Performance du contenu',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Performance du contenu'
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem: any) {
                return `${tooltipItem.label}: ${tooltipItem.raw} vues`;
              }
            }
          },
          legend: {
            display: false
          }
        }
      }
    });
  }
}
