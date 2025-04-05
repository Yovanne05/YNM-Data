import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-user-engagement-chart',
  standalone: true,
  imports: [],
  templateUrl: './user-engagement-chart.component.html',
  styleUrl: './user-engagement-chart.component.scss'
})
export class UserEngagementChartComponent implements OnChanges {
  @Input() userEngagement: any;
  private chart: Chart | null = null;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['userEngagement'] && this.userEngagement) {
      this.renderChart();
    }
  }

  renderChart(): void {
    const ctx = document.getElementById('userEngagementChart') as HTMLCanvasElement;
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const users = this.userEngagement?.users || [];
    const labels = users.map((user: { user_id: any; }) => `Utilisateur ${user.user_id}`);
    const viewCounts = users.map((user: { total_views: any; }) => user.total_views);
    const avgDurations = users.map((user: { avg_duration_minutes: string; }) => parseFloat(user.avg_duration_minutes));

    this.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Nombre de vues',
            data: viewCounts,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Durée moyenne (min)',
            data: avgDurations,
            backgroundColor: 'rgba(255, 206, 86, 0.6)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Engagement par utilisateur'
          },
          tooltip: {
            callbacks: {
              label: function(tooltipItem: any) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw}`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Valeur'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Utilisateurs'
            }
          }
        }
      }
    });
  }
}
