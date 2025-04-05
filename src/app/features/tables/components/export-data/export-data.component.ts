import { Component, inject, Input } from '@angular/core';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { CsvExtractService } from '../../../../services/transactional/csv-extract.service';

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
  @Input() tableName!: string;

  showErrorMessage: boolean = false;

  //TODO: Permettre de retirer tous les filtres avant l'export
  //TODO: Permettre d'exporter les données en format MySQL/PostgreSQL

  exportCsv() {
    if (this.tablesData && this.tablesData.length != 0) {
      this.csvExtractService.exportToCsv(this.tableName + '.csv', this.tablesData);
      this.showErrorMessage = false;
    }
    else {
      this.showErrorMessage = true;
    }
  }

}
