import { Component, inject, Input } from '@angular/core';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { CsvExtractService } from '../../../../services/csv-extract.service';

@Component({
  selector: 'app-export-data',
  standalone: true,
  imports: [TableCardDataComponent],
  templateUrl: './export-data.component.html',
  styleUrl: './export-data.component.scss'
})
export class ExportDataComponent {
  private readonly csvExtractService = inject(CsvExtractService)

  @Input() tablesData!: Record<string, string>[] | null;
  exportCsv() {
    console.log("Bouton cliqué")
    if (this.tablesData) {
      this.csvExtractService.exportToCsv('export.csv', this.tablesData);
    }
  }
  
}
