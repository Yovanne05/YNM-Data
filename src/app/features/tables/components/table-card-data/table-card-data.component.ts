import { Component, EventEmitter, Input, OnChanges, SimpleChanges, inject, output, ChangeDetectorRef, OnDestroy } from '@angular/core';
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
  imports: [ReactiveFormsModule, TableFiltersComponent, TableHeaderComponent, TableRowComponent],
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss']
})
export class TableCardDataComponent implements OnChanges, OnDestroy {
  private filterRegistry = inject(FilterRegistryService);
  private genericTableService = inject(GenericTableService);
  private cdr = inject(ChangeDetectorRef);
  private dataSubscription?: Subscription;

  @Input() tableName!: string;
  @Input() data: any[] = [];
  @Input() filters: any[] = [];

  editForm = new FormGroup({});
  showFilters = false;
  filterForm: FormGroup = new FormGroup({});
  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];
  editingItem: any = null;
  tempItemForm: FormGroup = new FormGroup({});
  filteredData: any[] = [];

  filterSubmit = output<void>();
  filterReset = output<void>();
  itemEdited = output<any>();
  itemDeleted = output<any>();
  sortChanged = output<{key: string, direction: 'asc' | 'desc'}[]>();
  sendTablesData = new EventEmitter<any[]>();

  ngOnChanges(changes: SimpleChanges): void {
    console.log('Data changed:', this.data);
    if (changes['data']) {
      this.filteredData = [...this.data];
      this.applySort();
    }
    if (changes['filters'] || changes['tableName']) {
      this.loadFilters();
    }
  }

  ngOnDestroy(): void {
    this.dataSubscription?.unsubscribe();
  }

  toggleFilters() {
    this.showFilters = !this.showFilters;
    this.cdr.detectChanges();
  }

  onSort(key: string) {
    const existingSort = this.sortKeys.find(s => s.key === key);

    if (existingSort) {
      existingSort.direction = existingSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKeys = [{ key, direction: 'asc' }];
    }

    this.applySort();
    this.sortChanged.emit(this.sortKeys);
  }

  private applySort() {
    if (this.sortKeys.length === 0 || !this.filteredData) return;

    const sortedData = [...this.filteredData].sort((a, b) => {
      for (const sort of this.sortKeys) {
        const valA = a[sort.key];
        const valB = b[sort.key];

        if (valA < valB) return sort.direction === 'asc' ? -1 : 1;
        if (valA > valB) return sort.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });

    this.filteredData = sortedData;
  }

  private initFilterForm() {
    const controls: Record<string, FormControl> = {};
    this.filters?.forEach(filter => {
      controls[filter.key] = new FormControl('');
      if (filter.type === 'number') {
        controls[`${filter.key}_operator`] = new FormControl('eq');
      }
    });
    this.filterForm = new FormGroup(controls);
  }

  private loadFilters(): void {
    this.filterRegistry.getFiltersForTable(this.tableName).subscribe({
      next: (filters) => {
        this.filters = filters;
        this.initFilterForm();
        this.loadDataWithFilters();
      },
      error: (err) => console.error('Error loading filters:', err)
    });
  }

  private loadDataWithFilters(): void {
    const activeFilters = this.getActiveFilters();

    this.dataSubscription = this.genericTableService.getTableData(this.tableName, activeFilters)
      .subscribe({
        next: (data) => {
          this.filteredData = [...data];
          this.applySort();
          this.sendTablesData.emit([...data]);
          this.cdr.detectChanges();
        },
        error: (err) => console.error('Error loading filtered data:', err)
      });
  }

  private getActiveFilters(): { [key: string]: { operator: string, value: any } } {
    const filters: { [key: string]: { operator: string, value: any } } = {};

    Object.keys(this.filterForm.controls).forEach(key => {
      if (key.endsWith('_operator')) return;

      const value = this.filterForm.get(key)?.value;
      if (value !== null && value !== undefined && value !== '') {
        const operatorControl = this.filterForm.get(`${key}_operator`);
        filters[key] = {
          operator: operatorControl?.value || 'eq',
          value: value
        };
      }
    });

    return filters;
  }

  onSubmitFilters() {
    this.loadDataWithFilters();
    this.filterSubmit.emit();
  }

  onResetFilters() {
    this.filterForm.reset();
    this.loadDataWithFilters();
    this.filterReset.emit();
  }

  startEditing(item: any) {
    this.editingItem = item;
    this.tempItemForm = new FormGroup({});

    this.getObjectKeys(item).forEach(key => {
      this.tempItemForm.addControl(key, new FormControl(item[key]));
    });
  }

  saveChanges() {
    if (this.tempItemForm.valid && this.editingItem) {
      const updatedItem = { ...this.editingItem, ...this.tempItemForm.value };

      this.genericTableService.updateItem(this.tableName, this.editingItem, updatedItem)
        .subscribe({
          next: () => {
            this.loadDataWithFilters();
            this.cancelEditing();
            this.cdr.detectChanges();
          },
          error: (err) => console.error('Error updating item:', err)
        });
    }
  }

  cancelEditing() {
    this.editingItem = null;
    this.tempItemForm = new FormGroup({});
    this.cdr.detectChanges();
  }

  onDelete(item: any) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
      this.genericTableService.deleteItem(this.tableName, item)
        .subscribe({
          next: () => {
            this.loadDataWithFilters();
            this.cdr.detectChanges();
          },
          error: (err) => console.error('Error deleting item:', err)
        });
    }
  }

  getObjectKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }
}
