import {
  Component,
  inject,
  Input,
  OnChanges,
  SimpleChanges,
  OnInit,
  Output,
  EventEmitter,
} from '@angular/core';
import { Observable } from 'rxjs';
import { getObjectKeys, getValue } from '../../../../utils/json.method';
import { FilterRegistryService } from '../../../../services/filter.registry.service';
import { FilterManagerService } from '../../../../services/filter.manager.service';
import { GenericTableService } from '../../../../services/generic.service';
import { CsvExtractService } from '../../../../services/csv-extract.service';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent implements OnInit, OnChanges {
  private readonly genericTableService = inject(GenericTableService);
  private readonly filterRegistry = inject(FilterRegistryService);
  private readonly filterManager = inject(FilterManagerService);
  private readonly csvExtractService = inject(CsvExtractService)

  @Input() tableName!: string;

  tablesData$!: Observable<Record<string, string>[]>;
  tablesData: Record<string, string>[] | null = null;
  filteredData: Record<string, string>[] | null = null;

  activeFilters: { [key: string]: boolean } = {};
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;

  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];

  @Output() sendTablesData = new EventEmitter<Record<string, string>[] | null>

  ngOnInit(): void {
    this.loadData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['tableName']?.currentValue) {
      this.resetState();
      this.loadData();
    }
  }

  private resetState(): void {
    this.activeFilters = {};
    this.sortKeys = [];
    this.filteredData = null;
  }

  private loadData(): void {
    this.tablesData$ = this.genericTableService.getTableData(this.tableName);

    this.tablesData$.subscribe({
      next: (data) => {
        if (data) {
          this.tablesData = data;
          this.availableFilters = this.getAvailableFilters();
          this.applyFiltersAndSort();
          this.sendTablesData.emit(this.tablesData);
        }
      },
      error: (err) => console.error('Erreur de souscription:', err),
    });
  }

  private getAvailableFilters(): { key: string; name: string }[] {
    const filters = this.filterRegistry.getFiltersForTable(this.tableName);
    return Object.entries(filters).map(([key, name]) => ({ key, name }));
  }

  private applyFiltersAndSort(): void {
    if (!this.tablesData) return;

    this.filteredData = this.filterManager.applyFilters(
      this.tablesData,
      this.activeFilters
    );

    if (this.sortKeys.length > 0) {
      this.filteredData = this.sortData(this.filteredData);
    }
  }

  private sortData(data: Record<string, string>[]): Record<string, string>[] {
    return data.sort((a, b) => {
      for (const sortKey of this.sortKeys) {
        const valueA = a[sortKey.key];
        const valueB = b[sortKey.key];

        if (valueA < valueB) return sortKey.direction === 'asc' ? -1 : 1;
        if (valueA > valueB) return sortKey.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }

  onSort(key: string): void {
    const existingSortKeyIndex = this.sortKeys.findIndex(
      (sort) => sort.key === key
    );

    if (existingSortKeyIndex !== -1) {
      const existingSortKey = this.sortKeys[existingSortKeyIndex];
      existingSortKey.direction =
        existingSortKey.direction === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKeys.push({ key, direction: 'asc' });
    }

    this.applyFiltersAndSort();
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  onFilterSelect(filterKey: string): void {
    this.activeFilters[filterKey] = !this.activeFilters[filterKey];
    this.applyFiltersAndSort();
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return getObjectKeys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return getValue(key, item);
  }
}