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

  @Input() tableName!: string;

  ngOnInit(): void {
    this.loadData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['tableName'] && changes['tableName'].currentValue) {
      this.activeFilters = {};
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
            console.log(this.activeFilters);
            this.filteredData = this.filterManager.applyFilters(data, this.activeFilters);
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
