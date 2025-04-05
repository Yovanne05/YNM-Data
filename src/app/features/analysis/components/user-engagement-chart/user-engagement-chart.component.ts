import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ChartBaseComponent } from '../../utils/base-chart';

@Component({
  selector: 'app-user-engagement-chart',
  standalone: true,
  imports: [],
  templateUrl: './user-engagement-chart.component.html',
  styleUrl: './user-engagement-chart.component.scss'
})
export class UserEngagementChartComponent extends ChartBaseComponent {
  @Input() set userEngagement(value: any) {
    this.chartData = value?.users || [];
  }

  protected override chartId = 'userEngagementChart';
  protected override chartType: 'bar' | 'line' | 'pie' | 'doughnut' = 'bar';
  protected override chartTitle = 'Engagement par utilisateur';

  protected override getChartConfig(): any {
    const labels = this.chartData.map((user: any) => `Utilisateur ${user.user_id}`);
    const viewCounts = this.chartData.map((user: any) => user.total_views);
    const avgDurations = this.chartData.map((user: any) => parseFloat(user.avg_duration_minutes));

    return {
      type: this.chartType,
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
        ...this.getDefaultOptions(),
        plugins: {
          ...this.getDefaultOptions().plugins,
          tooltip: {
            callbacks: {
              label: (tooltipItem: any) => `${tooltipItem.dataset.label}: ${tooltipItem.raw}`
            }
          }
        },
        scales: {
          ...this.getDefaultOptions().scales,
          y: {
            ...this.getDefaultOptions().scales?.y,
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
    };
  }
}
