import { Component, inject, Input } from '@angular/core';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { CsvExtractService } from '../../../../services/transactional/csv-extract.service';
import {MatIconModule} from "@angular/material/icon";
import { GenericTableService } from '../../../../services/transactional/generic.service';
import { TableFilterService } from '../../../../services/transactional/tables/table.filter.service';

@Component({
  selector: 'app-export-data',
  standalone: true,
  imports: [TableCardDataComponent, MatIconModule],
  templateUrl: './export-data.component.html',
  styleUrl: './export-data.component.scss',
  providers: [TableFilterService]
})
export class ExportDataComponent {
  private readonly csvExtractService = inject(CsvExtractService)
  private readonly genericService = inject(GenericTableService)
  private readonly filterService = inject(TableFilterService)

  @Input() tableName!: string;
  tableData!: Record<string, string>[];
  showErrorMessage: boolean = false;

  ngOnInit(): void {
    this.genericService.getTableDataNoPagination(this.tableName, this.filterService.getActiveFilters()).subscribe({
      next: (data) => {
        this.tableData = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des données :', err);
        this.showErrorMessage = true;
      }
    });
  }

  ngOnChanges(): void {
    this.genericService.getTableDataNoPagination(this.tableName, this.filterService.getActiveFilters()).subscribe({
      next: (data) => {
        this.tableData = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des données :', err);
        this.showErrorMessage = true;
      }
    });
  }

  exportCsv() {
    if (this.tableData && this.tableData.length != 0) {
      this.csvExtractService.exportToCsv(this.tableName + '.csv', this.tableData);
      this.showErrorMessage = false;
    }
    else {
      this.showErrorMessage = true;
    }
  }

}
