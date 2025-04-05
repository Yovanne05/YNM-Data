import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-top-content-chart',
  standalone: true,
  imports: [],
  templateUrl: './top-content-chart.component.html',
  styleUrl: './top-content-chart.component.scss'
})
export class TopContentChartComponent implements OnChanges {
  @Input() topContent: any[] = [];
  private chart: Chart | null = null;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['topContent'] && this.topContent) {
      this.renderChart();
    }
  }

  renderChart(): void {
    const ctx = document.getElementById('topContentChart') as HTMLCanvasElement;
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const labels = this.topContent.map(item => item.content_title);
    const data = this.topContent.map(item => item.view_count);

    this.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Nombre de visionnages',
          data: data,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Top 3 des contenus les plus regardés'
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Nombre de visionnages'
            }
          }
        }
      }
    });
  }
}
