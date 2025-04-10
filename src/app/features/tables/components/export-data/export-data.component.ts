import {Component, inject, Input} from '@angular/core';
import { CsvExtractService } from '../../../../services/transactional/csv-extract.service';
import { MatIconModule } from "@angular/material/icon";
import { GenericTableService } from '../../../../services/transactional/generic.service';
import { TableFilterService } from '../../../../services/transactional/tables/table.filter.service';
import { TableSortService } from '../../../../services/transactional/tables/table.sort.service';

@Component({
  selector: 'app-export-data',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './export-data.component.html',
  styleUrl: './export-data.component.scss',
})
export class ExportDataComponent {
  private csvExtractService = inject(CsvExtractService);
  private genericService = inject(GenericTableService);
  private filterService = inject(TableFilterService);
  private sortService = inject(TableSortService);

  @Input() tableName!: string;
  showErrorMessage: boolean = false;

  exportCsv() {
    const activeFilters = this.filterService.getActiveFilters();
    const sortKeys = this.sortService.sortKeys;
    console.log(activeFilters, sortKeys)

    const filterParams: Record<string, string> = {};

    Object.keys(activeFilters).forEach(key => {
      const filter = activeFilters[key];
      filterParams[`${key}__${filter.operator}`] = filter.value;
    });

    const sortParams: Record<string, string> = {};
    sortKeys.forEach(sort => {
      sortParams[`sort_${sort.key}`] = sort.direction;
    });

    const allParams = { ...filterParams, ...sortParams };
    this.genericService.getTableDataNoPagination(
      this.tableName,
      allParams
    ).subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          this.csvExtractService.exportToCsv(`${this.tableName}_export.csv`, data);
          this.showErrorMessage = false;
        } else {
          this.showErrorMessage = true;
        }
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des données :', err);
        this.showErrorMessage = true;
      }
    });
  }
}
