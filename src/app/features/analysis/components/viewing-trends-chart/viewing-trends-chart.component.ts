import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ChartBaseComponent } from '../../utils/base-chart';

@Component({
  selector: 'app-viewing-trends-chart',
  standalone: true,
  imports: [],
  templateUrl: './viewing-trends-chart.component.html',
  styleUrl: './viewing-trends-chart.component.scss'
})
export class ViewingTrendsChartComponent extends ChartBaseComponent {
  @Input() set viewingTrends(value: any[]) {
    this.chartData = value;
  }

  protected override chartId = 'viewingTrendsChart';
  protected override chartType: 'line' = 'line';
  protected override chartTitle = 'Tendances de visionnage';

  protected override getChartConfig(): any {
    const periodMap = new Map<string, number>();
    this.chartData.forEach(item => {
      const total = periodMap.get(item.period) || 0;
      periodMap.set(item.period, item.view_count);
    });

    const labels = Array.from(periodMap.keys());
    const data = Array.from(periodMap.values());

    return {
      type: this.chartType,
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
        ...this.getDefaultOptions(),
        scales: {
          ...this.getDefaultOptions().scales,
          y: {
            ...this.getDefaultOptions().scales?.y,
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
    };
  }
}
