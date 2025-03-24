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
import { GenericTableService } from '../../../../services/generic.service';
import { FormsModule, ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { CsvExtractService } from '../../../../services/csv-extract.service';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule],
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent implements OnInit, OnChanges {
  private readonly genericTableService = inject(GenericTableService);
  private readonly filterRegistry = inject(FilterRegistryService);

  @Input() tableName!: string;

  tablesData$!: Observable<Record<string, string>[]>;

  filteredData: Record<string, string>[] | null = null;
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;
  filterForm: FormGroup = new FormGroup({});

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
    this.filteredData = null;
    this.sortKeys = [];
    this.filterForm.reset();
  }

  private loadData(): void {
    const activeFilters = this.getActiveFilters();
    this.tablesData$ = this.genericTableService.getTableData(this.tableName, activeFilters);

    this.tablesData$.subscribe({
      next: (data) => {
        if (data) {
          this.filteredData = this.applySort(data);
          this.availableFilters = this.getAvailableFilters();
          this.initFilterForm();
          this.sendTablesData.emit(this.filteredData);
        }
      },
      error: (err) => console.error('Erreur de souscription:', err),
    });
  }

  private getActiveFilters(): { [key: string]: string } {
    return Object.fromEntries(
      Object.entries(this.filterForm.value).filter(([_, value]) => value).map(([key, value]) => [key, value as string])
    );
  }

  private getAvailableFilters(): { key: string; name: string }[] {
    const filters = this.filterRegistry.getFiltersForTable(this.tableName);
    return Object.entries(filters).map(([key, name]) => ({ key, name }));
  }

  private initFilterForm(): void {
    const formControls: { [key: string]: FormControl } = {};
    this.availableFilters.forEach((filter) => {
      formControls[filter.key] = new FormControl('');
      formControls[filter.key + '_isGreaterThan'] = new FormControl(false);
    });
    this.filterForm = new FormGroup(formControls);
  }

  private applySort(data: Record<string, string>[]): Record<string, string>[] {
    if (this.sortKeys.length === 0) return data;

    return data.sort((a, b) => {
      for (const { key, direction } of this.sortKeys) {
        const valueA = a[key];
        const valueB = b[key];

        if (valueA < valueB) return direction === 'asc' ? -1 : 1;
        if (valueA > valueB) return direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }

  onSort(key: string): void {
    const existingSortKey = this.sortKeys.find((sort) => sort.key === key);

    if (existingSortKey) {
      existingSortKey.direction = existingSortKey.direction === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKeys.push({ key, direction: 'asc' });
    }

    if (this.filteredData) {
      this.filteredData = this.applySort(this.filteredData);
    }
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  onSubmit(): void {
    this.loadData();
  }

  getObjectKeys = getObjectKeys;
  getValue = getValue;
}
