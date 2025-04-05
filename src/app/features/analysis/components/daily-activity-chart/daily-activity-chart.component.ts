import { Component, Input, OnInit } from '@angular/core';
import { Chart} from 'chart.js';

@Component({
  selector: 'app-daily-activity-chart',
  standalone: true,
  imports: [],
  templateUrl: './daily-activity-chart.component.html',
  styleUrl: './daily-activity-chart.component.scss'
})
export class DailyActivityChartComponent implements OnInit {
  @Input() dailyActivity: any[] = [];

  ngOnInit(): void {
    this.renderChart();
  }

  renderChart(): void {
    const ctx = document.getElementById('dailyActivityChart') as HTMLCanvasElement;
    if (!ctx) return;

    const existingChart = Chart.getChart(ctx);
    if (existingChart) {
      existingChart.destroy();
    }

    const labels = this.dailyActivity.map(item => item.date);
    const data = this.dailyActivity.map(item => item.view_count);

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Activité quotidienne',
          data: data,
          fill: false,
          borderColor: 'rgba(153, 102, 255, 1)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Activité quotidienne des utilisateurs'
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Nombre de vues'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Date'
            }
          }
        }
      }
    });
  }
}
