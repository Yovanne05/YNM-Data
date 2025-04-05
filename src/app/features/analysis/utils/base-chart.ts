import { Input, OnChanges, SimpleChanges } from "@angular/core";
import { Chart, ChartType, registerables } from "chart.js";
import { Component } from "@angular/core";

@Component({
  selector: 'app-base-chart',
  template: ''
})

export abstract class BaseChartComponent implements OnChanges {
  @Input() chartData: any;
  protected chart: Chart | null = null;

  protected abstract chartId: string;
  protected abstract chartType: ChartType;
  protected abstract chartTitle: string;

  constructor() {
    Chart.register(...registerables);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['chartData'] && this.chartData) {
      this.renderChart();
    }
  }

  protected abstract getChartData(): any;

  protected getChartOptions(): any {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: this.chartTitle
        }
      }
    };
  }

  protected renderChart(): void {
    const ctx = document.getElementById(this.chartId) as HTMLCanvasElement;
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
    }

    this.chart = new Chart(ctx, {
      type: this.chartType,
      data: this.getChartData(),
      options: this.getChartOptions()
    });
  }

  ngOnDestroy(): void {
    if (this.chart) {
      this.chart.destroy();
    }
  }
}
