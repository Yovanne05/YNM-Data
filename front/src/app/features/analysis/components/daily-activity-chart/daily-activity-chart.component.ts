import { Component, Input, OnInit } from '@angular/core';
import { Chart} from 'chart.js';
import { ChartBaseComponent } from '../../utils/base-chart';

@Component({
  selector: 'app-daily-activity-chart',
  standalone: true,
  imports: [],
  templateUrl: './daily-activity-chart.component.html',
  styleUrl: './daily-activity-chart.component.scss'
})
export class DailyActivityChartComponent extends ChartBaseComponent {
  @Input() set dailyActivity(data: any[]) {
    this.chartData = data;
  }


  protected chartId = 'dailyActivityChart';
  protected chartType = 'line' as const;
  protected chartTitle = 'Activité quotidienne des utilisateurs';

  protected getChartConfig() {
    const labels = this.chartData.map(item => item.date);
    const data = this.chartData.map(item => item.view_count);

    return {
      type: this.chartType,
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
      options: this.getDefaultOptions()
    };
  }
}
