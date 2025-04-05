import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ChartBaseComponent } from '../../utils/base-chart';

@Component({
  selector: 'app-content-performance-chart',
  standalone: true,
  imports: [],
  templateUrl: './content-performance-chart.component.html',
  styleUrl: './content-performance-chart.component.scss'
})
export class ContentPerformanceChartComponent extends ChartBaseComponent {
  @Input() set contentPerformance(value: any[]) {
    this.chartData = value;
  }

  protected override chartId = 'contentPerformanceChart';
  protected override chartType: 'pie' = 'pie';
  protected override chartTitle = 'Performance du contenu';

  protected override getChartConfig(): any {
    const labels = this.chartData.map(item => item.content_title);
    const data = this.chartData.map(item => item.view_count);

    return {
      type: this.chartType,
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
        ...this.getDefaultOptions(),
        plugins: {
          ...this.getDefaultOptions().plugins,
          tooltip: {
            callbacks: {
              label: (tooltipItem: any) => `${tooltipItem.label}: ${tooltipItem.raw} vues`
            }
          },
          legend: {
            display: false
          }
        }
      }
    };
  }
}
