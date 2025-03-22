import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ServiceFactory } from '../../../../services/service-factory';
import { getObjectKeys, getValue } from '../../../../utils/json.method';
import { FilterStrategy } from '../../../../models/interface/filter.interface';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent implements OnInit, OnChanges {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$!: Observable<Record<string, string>[]>;
  tablesData: Record<string, string>[] | null = null;
  filteredData: Record<string, string>[] | null = null;

  activeFilters: { [key: string]: boolean } = {};
  availableFilters: string[] = [];

  @Input() tableName!: string;

  ngOnInit(): void {
    this.loadData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['tableName'] && changes['tableName'].currentValue) {
      this.loadData();
    }
  }

  private loadData(): void {
    const service = this.serviceFactory.getService(this.tableName);

    if (service) {

      this.tablesData$ = service.service.getTableData() as unknown as Observable<Record<string, string>[]>;
      this.availableFilters = Object.keys(service.filters);

      this.tablesData$.subscribe({
        next: (data: Record<string, string>[]) => {
          if (data) {
            this.tablesData = data;
            this.filteredData = this.applyFilters(data, service.filters);
            console.log("Données filtrées : ", this.filteredData);
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

  onFilterSelect(filterKey: string): void {
    this.activeFilters[filterKey] = !this.activeFilters[filterKey];
    this.loadData();
  }

  private applyFilters(data: Record<string, string>[], filters: { [key: string]: FilterStrategy }): Record<string, string>[] {
    let filteredData = data;

    Object.keys(this.activeFilters).forEach(filterKey => {
      if (this.activeFilters[filterKey]) {
        const filter = filters[filterKey];
        if (filter) {
          filteredData = filter.filter(filteredData);
        }
      }
    });

    return filteredData;
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return getObjectKeys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return getValue(key, item);
  }
}
