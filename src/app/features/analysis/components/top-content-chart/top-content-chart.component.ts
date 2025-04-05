import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ChartBaseComponent } from '../../utils/base-chart';

@Component({
  selector: 'app-top-content-chart',
  standalone: true,
  imports: [],
  templateUrl: './top-content-chart.component.html',
  styleUrl: './top-content-chart.component.scss'
})
export class TopContentChartComponent extends ChartBaseComponent {
  @Input() set topContent(value: any[]) {
    this.chartData = value;
  }

  protected override chartId = 'topContentChart';
  protected override chartType: 'bar' = 'bar';
  protected override chartTitle = 'Top 3 des contenus les plus regardés';

  protected override getChartConfig(): any {
    const labels = this.chartData.map(item => item.content_title);
    const data = this.chartData.map(item => item.view_count);

    return {
      type: this.chartType,
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
        ...this.getDefaultOptions(),
        scales: {
          ...this.getDefaultOptions().scales,
          y: {
            ...this.getDefaultOptions().scales?.y,
            title: {
              display: true,
              text: 'Nombre de visionnages'
            }
          }
        }
      }
    };
  }
}
