import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  SimpleChanges,
  inject,
  output,
} from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { TableFiltersComponent } from '../table-filters/table-filters.component';
import { TableHeaderComponent } from '../table-header/table-header.component';
import { TableRowComponent } from '../table-row/table-row.component';
import { FilterRegistryService } from '../../../../services/filter.registry.service';
import { GenericTableService } from '../../../../services/generic.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    TableFiltersComponent,
    TableHeaderComponent,
    TableRowComponent,
  ],
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent implements OnChanges {
  private filterRegistry = inject(FilterRegistryService);
  private genericTableService = inject(GenericTableService);
  private dataSubscription?: Subscription;

  @Input() tableName!: string;
  @Input() data: any[] = [];
  @Input() filters: any[] = [];

  editForm = new FormGroup({});
  filterForm: FormGroup = new FormGroup({});
  tempItemForm: FormGroup = new FormGroup({});

  showFilters = false;
  editingItem: any = null;
  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];
  filteredData: any[] = [];

  filterSubmit = output<void>();
  filterReset = output<void>();
  itemEdited = output<any>();
  itemDeleted = output<any>();
  sortChanged = output<{ key: string; direction: 'asc' | 'desc' }[]>();
  sendTablesData = new EventEmitter<any[]>();

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data'] && this.data.length > 0) {
      this.handleDataInput();
    }
    if (changes['filters'] || changes['tableName']) {
      this.loadFilters();
    }
  }

  private handleDataInput(): void {
    this.filteredData = [...this.data];
    this.applySort();
  }

  private loadDataWithFilters(): void {
    const requestParams = this.buildRequestParams();

    this.dataSubscription = this.genericTableService
      .getTableData(this.tableName, requestParams)
      .subscribe({
        next: (data) => this.handleDataResponse(data),
        error: (err) => console.error('Error loading filtered data:', err),
      });
  }

  private buildRequestParams(): any {
    const activeFilters = this.getActiveFilters();
    const sortParams = this.sortKeys.reduce((acc, sort) => {
      acc[sort.key] = { operator: sort.direction, value: '' };
      return acc;
    }, {} as { [key: string]: { operator: string; value: string } });

    return { ...activeFilters, ...sortParams };
  }

  private handleDataResponse(data: any[]): void {
    this.filteredData = [...data];
    this.sendTablesData.emit([...this.filteredData]);
  }

  private loadFilters(): void {
    this.filterRegistry.getFiltersForTable(this.tableName).subscribe({
      next: (filters) => this.handleFiltersResponse(filters),
      error: (err) => console.error('Error loading filters:', err),
    });
  }

  private handleFiltersResponse(filters: any[]): void {
    this.filters = filters;
    this.initFilterForm();
    this.loadDataWithFilters();
  }

  private initFilterForm(): void {
    const controls: Record<string, FormControl> = {};
    this.filters?.forEach((filter) => {
      controls[filter.key] = new FormControl('');
      if (filter.type === 'number') {
        controls[`${filter.key}_operator`] = new FormControl('eq');
      }
    });
    this.filterForm = new FormGroup(controls);
  }

  private getActiveFilters(): {
    [key: string]: { operator: string; value: any };
  } {
    const filters: { [key: string]: { operator: string; value: any } } = {};

    Object.keys(this.filterForm.controls).forEach((key) => {
      if (key.endsWith('_operator')) return;

      const value = this.filterForm.get(key)?.value;
      if (value !== null && value !== undefined && value !== '') {
        const operatorControl = this.filterForm.get(`${key}_operator`);
        filters[key] = {
          operator: operatorControl?.value || 'eq',
          value: value,
        };
      }
    });

    return filters;
  }

  private applySort(): void {
    if (this.filteredData && this.sortKeys.length > 0) {
      this.filteredData = [...this.filteredData].sort((a, b) =>
        this.multiColumnSortComparator(a, b)
      );
    }
  }

  private multiColumnSortComparator(a: any, b: any): number {
    for (const sort of this.sortKeys) {
      const comparisonResult = this.compareStrings(
        a[sort.key],
        b[sort.key],
        sort.direction
      );
      if (comparisonResult !== 0) return comparisonResult;
    }
    return 0;
  }

  /**
   * Compare deux valeurs de type string avec prise en compte de la direction de tri
   */
  private compareStrings(
    a: string,
    b: string,
    direction: 'asc' | 'desc'
  ): number {
    if (a === b) return 0;

    if (!a || !b) {
      if (!a && !b) return 0;
      return !a ? (direction === 'asc' ? -1 : 1) : direction === 'asc' ? 1 : -1;
    }

    // Comparaison des strings
    const comparison = a.localeCompare(b);
    return direction === 'asc' ? comparison : -comparison;
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  onSort(key: string): void {
    const existingSortIndex = this.sortKeys.findIndex((s) => s.key === key);

    if (existingSortIndex !== -1) {
      const currentDirection = this.sortKeys[existingSortIndex].direction;
      currentDirection === 'asc'
        ? (this.sortKeys[existingSortIndex].direction = 'desc')
        : this.sortKeys.splice(existingSortIndex, 1);
    } else {
      this.sortKeys.push({ key, direction: 'asc' });
    }

    this.loadDataWithFilters();
    this.sortChanged.emit(this.sortKeys);
  }

  removeSort(key: string): void {
    this.sortKeys = this.sortKeys.filter((s) => s.key !== key);
    this.loadDataWithFilters();
    this.sortChanged.emit(this.sortKeys);
  }

  clearAllSorts(): void {
    this.sortKeys = [];
    this.loadDataWithFilters();
    this.sortChanged.emit([]);
  }

  onSubmitFilters(): void {
    this.loadDataWithFilters();
    this.filterSubmit.emit();
  }

  onResetFilters(): void {
    this.filterForm.reset();
    this.loadDataWithFilters();
    this.filterReset.emit();
  }

  startEditing(item: any): void {
    this.editingItem = item;
    this.tempItemForm = new FormGroup({});
    this.getObjectKeys(item).forEach((key) => {
      this.tempItemForm.addControl(key, new FormControl(item[key]));
    });
  }

  saveChanges(): void {
    if (this.tempItemForm.valid && this.editingItem) {
      const updatedItem = { ...this.editingItem, ...this.tempItemForm.value };
      this.genericTableService
        .updateItem(this.tableName, this.editingItem, updatedItem)
        .subscribe({
          next: () => {
            this.loadDataWithFilters();
            this.cancelEditing();
          },
          error: (err) => console.error('Error updating item:', err),
        });
    }
  }

  cancelEditing(): void {
    this.editingItem = null;
    this.tempItemForm = new FormGroup({});
  }

  onDelete(item: any): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
      this.genericTableService.deleteItem(this.tableName, item).subscribe({
        next: () => this.loadDataWithFilters(),
        error: (err) => console.error('Error deleting item:', err),
      });
    }
  }

  getObjectKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }

  getSortDirection(key: string): 'asc' | 'desc' | null {
    const sort = this.sortKeys.find((s) => s.key === key);
    return sort ? sort.direction : null;
  }

  getSortOrder(key: string): number | null {
    const index = this.sortKeys.findIndex((s) => s.key === key);
    return index >= 0 ? index + 1 : null;
  }
}
