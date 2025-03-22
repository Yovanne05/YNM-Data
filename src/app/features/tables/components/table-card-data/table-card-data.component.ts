import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { getObjectKeys, getValue } from '../../../../utils/json.method';
import { FilterRegistryService } from '../../../../services/filter.registry.service';
import { FilterManagerService } from '../../../../services/filter.manager.service';
import { GenericTableService } from '../../../../services/generic.service';

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

  tablesData$!: Observable<Record<string, string>[]>;
  tablesData: Record<string, string>[] | null = null;

  filteredData: Record<string, string>[] | null = null;
  activeFilters: { [key: string]: boolean } = {};
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;

  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];
  sortDirection: 'asc' | 'desc' = 'asc';

  @Input() tableName!: string;

  ngOnInit(): void {
    this.loadData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['tableName'] && changes['tableName'].currentValue) {
      this.activeFilters = {};
      this.sortKeys = [];
      this.loadData();
    }
  }

  private loadData(): void {
    const tableData = this.genericTableService.getTableData(this.tableName);
    this.tablesData$ = tableData;
    if (this.tablesData$) {
      this.availableFilters = Object.entries(this.filterRegistry.getFiltersForTable(this.tableName)).map(([key, name]) => ({
        key,
        name,
      }));

      this.tablesData$.subscribe({
        next: (data: Record<string, string>[]) => {
          if (data) {
            this.tablesData = data;
            this.filteredData = this.filterManager.applyFilters(data, this.activeFilters);
            if (this.sortKeys) {
              this.filteredData = this.sortData(this.filteredData);
            }
          }
        },
        error: (err) => {
          console.error('Erreur de souscription:', err);
        },
      });
    } else {
      console.error('Aucun service trouvé pour cette table:', this.tableName);
    }
  }

  private sortData(data: Record<string, string>[]): Record<string, string>[] {
    if (this.sortKeys.length === 0) return data;

    return data.sort((a, b) => {
      for (const sortKey of this.sortKeys) {
        const valueA = a[sortKey.key];
        const valueB = b[sortKey.key];

        if (valueA < valueB) {
          return sortKey.direction === 'asc' ? -1 : 1;
        }
        if (valueA > valueB) {
          return sortKey.direction === 'asc' ? 1 : -1;
        }
      }
      return 0;
    });
  }

  onSort(key: string): void {
    const existingSortKeyIndex = this.sortKeys.findIndex(sort => sort.key === key);

    if (existingSortKeyIndex !== -1) {
      const existingSortKey = this.sortKeys[existingSortKeyIndex];
      if (existingSortKey.direction === 'asc') {
        existingSortKey.direction = 'desc';
      } else {
        this.sortKeys.splice(existingSortKeyIndex, 1);
      }
    } else {
      this.sortKeys.push({ key, direction: 'asc' });
    }

    this.loadData();
  }

  toggleFilters() {
    this.showFilters = !this.showFilters;
  }

  onFilterSelect(filterKey: string): void {
    this.activeFilters[filterKey] = !this.activeFilters[filterKey];
    this.loadData();
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return getObjectKeys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return getValue(key, item);
  }
}
