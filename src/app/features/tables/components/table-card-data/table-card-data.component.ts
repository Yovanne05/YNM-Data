import { Component, EventEmitter, Input, OnChanges, SimpleChanges, inject, output, OnDestroy, HostListener } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { TableFiltersComponent } from '../table-filters/table-filters.component';
import { TableHeaderComponent } from '../table-header/table-header.component';
import { TableRowComponent } from '../table-row/table-row.component';
import { FilterRegistryService } from '../../../../services/transactional/filter.registry.service';
import { GenericTableService } from '../../../../services/transactional/generic.service';
import { Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';
import { MatIcon } from "@angular/material/icon";
import {isIdColumn, getUserFriendlyError} from "../../utils/table-utils";
import {TableSortService} from "../../../../services/transactional/tables/table.sort.service";
import {TableFilterService} from "../../../../services/transactional/tables/table.filter.service";
import {TablePaginationService} from "../../../../services/transactional/tables/table.pagination.service";

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    TableFiltersComponent,
    TableHeaderComponent,
    TableRowComponent,
    CommonModule,
    FormsModule,
    MatIcon
  ],
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
  providers: [GenericTableService, TableSortService, TableFilterService, TablePaginationService]
})
export class TableCardDataComponent implements OnChanges, OnDestroy {
  private filterRegistry = inject(FilterRegistryService);
  private dataService = inject(GenericTableService);
  private sortService = inject(TableSortService);
  private filterService = inject(TableFilterService);
  private paginationService = inject(TablePaginationService);
  private dataSubscription?: Subscription;

  @Input() tableName!: string;
  @Input() data: Record<string, string>[] = [];
  @Input() filters: Record<string, string>[] = [];

  tempItemForm: FormGroup = new FormGroup({});
  addForm: FormGroup = new FormGroup({});

  showFilters = false;
  editingItem: any = null;
  activeDropdown: any = null;
  isAddingMode = false;
  isLoading = false;
  errorMessage: string | null = null;
  newItem: {[key: string]: any} = {};
  requiredFields: string[] = [];
  fieldTypes: {[key: string]: {type: string, values?: string[]}} = {};

  filterSubmit = output<void>();
  filterReset = output<void>();
  itemEdited = output<any>();
  itemDeleted = output<any>();
  sortChanged = output<{ key: string; direction: 'asc' | 'desc' }[]>();
  sendTablesData = new EventEmitter<any[]>();

  get filteredData() {
    return this.paginationService.filteredData;
  }

  get paginationData() {
    return this.paginationService.paginationData;
  }

  get pageNumber() {
    return this.paginationService.pageNumber;
  }

  get actualPage() {
    return this.paginationService.actualPage;
  }

  get sortKeys() {
    return this.sortService.sortKeys;
  }

  get filterForm() {
    return this.filterService.filterForm;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data'] && this.data.length > 0) {
      this.paginationService.setData([...this.data]);
      this.applySort();
      this.activeDropdown = null;
    }
    if (changes['filters'] || changes['tableName']) {
      this.loadFilters();
    }
  }

  ngOnDestroy(): void {
    this.dataSubscription?.unsubscribe();
  }

  isIdColumn(column: string): boolean {
    return isIdColumn(column, this.tableName);
  }

  getObjectKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }

  getInputType(field: string): string {
    return this.fieldTypes[field]?.type || 'text';
  }

  getAddFormFields(): string[] {
    return this.addForm ? Object.keys(this.addForm.controls) : [];
  }

  isRequiredField(field: string): boolean {
    return this.requiredFields.includes(field);
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  @HostListener('document:click')
  closeDropdown(): void {
    this.activeDropdown = null;
  }

  onSort(key: string): void {
    this.sortService.onSort(key);
    this.applySort();
    this.sortChanged.emit([...this.sortKeys]);
  }

  private applySort(): void {
    this.paginationService.setData(this.sortService.applySort([...this.filteredData]));
  }

  private loadFilters(): void {
    this.filterRegistry.getFiltersForTable(this.tableName).subscribe({
      next: (filters) => {
        this.filters = filters;
        this.filterService.initFilterForm(this.filters);
        this.loadDataWithFilters();
      },
      error: (err) => console.error('Error loading filters:', err),
    });
  }

  private loadDataWithFilters(): void {
    const activeFilters = this.filterService.getActiveFilters();

    this.dataSubscription = this.dataService
      .getTableData(this.tableName, activeFilters)
      .subscribe({
        next: (data) => {
          this.paginationService.setData([...data]);
          this.applySort();
          this.sendTablesData.emit([...this.filteredData]);
        },
        error: (err) => console.error('Error loading filtered data:', err),
      });
  }

  onSubmitFilters(): void {
    this.loadDataWithFilters();
    this.filterSubmit.emit();
  }

  onResetFilters(): void {
    this.filterService.resetFilters();
    this.loadDataWithFilters();
    this.filterReset.emit();
  }

  startEditing(item: any): void {
    this.editingItem = item;
    this.tempItemForm = new FormGroup({});
    Object.keys(item).forEach((key) => {
      if (!this.isIdColumn(key)) {
        this.tempItemForm.addControl(key, new FormControl(item[key]));
      }
    });
  }

  saveChanges(): void {
    if (this.tempItemForm.valid && this.editingItem) {
      const updatedItem = { ...this.editingItem, ...this.tempItemForm.value };
      this.dataService.updateItem(this.tableName, this.editingItem, updatedItem)
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
      this.dataService.deleteItem(this.tableName, item).subscribe({
        next: () => this.loadDataWithFilters(),
        error: (err) => console.error('Error deleting item:', err),
      });
    }
  }

  startAdding(): void {
    this.isAddingMode = true;
    this.newItem = {};
    this.initAddForm();
    this.errorMessage = null;
    this.cancelEditing();
  }

  private async initAddForm(): Promise<void> {
    this.addForm = new FormGroup({});
    this.fieldTypes = {};

    if (this.filteredData.length > 0) {
      const sampleItem = this.filteredData[0];
      await this.loadColumnSchemas(sampleItem);

      Object.keys(sampleItem).forEach(key => {
        if (!this.isIdColumn(key)) {
          this.addForm.addControl(key, new FormControl(''));
          this.addForm.get(key)?.valueChanges.subscribe(value => {
            this.newItem[key] = value;
          });
        }
      });
    }
  }

  private async loadColumnSchemas(sampleItem: any): Promise<void> {
    const fields = Object.keys(sampleItem).filter(key => !this.isIdColumn(key));

    for (const field of fields) {
      try {
        const schema = await this.dataService.getColumnSchema(this.tableName, field).toPromise();
        this.fieldTypes[field] = schema;
      } catch (e) {
        console.error(`Failed to load schema for ${field}:`, e);
        this.fieldTypes[field] = { type: 'text' };
      }
    }
  }

  onAddSubmit(): void {
    if (this.addForm.valid) {
      this.isLoading = true;
      this.errorMessage = null;

      this.convertFormDataTypes();

      this.dataService.createItem(this.tableName, this.newItem)
        .subscribe({
          next: () => {
            this.isLoading = false;
            this.loadDataWithFilters();
            this.cancelAdding();
          },
          error: (err) => {
            this.isLoading = false;
            console.error('Détails complets de l\'erreur:', err);
            this.errorMessage = getUserFriendlyError(err);
          }
        });
    }
  }

  private convertFormDataTypes(): void {
    const formValue = this.addForm.value;

    const numericFields = ['id', 'age', 'prix', 'annee', 'duree', 'saison'];
    numericFields.forEach(field => {
      if (formValue[field] !== undefined) {
        this.addForm.get(field)?.setValue(Number(formValue[field]));
      }
    });

    const dateFields = ['dateDebutLicence', 'dateFinLicence'];
    dateFields.forEach(field => {
      if (formValue[field]) {
        const dateValue = new Date(formValue[field]).toISOString().split('T')[0];
        this.addForm.get(field)?.setValue(dateValue);
      }
    });
  }

  cancelAdding(): void {
    this.isAddingMode = false;
    this.addForm.reset();
    this.errorMessage = null;
  }

  nextPage(): void {
    this.paginationService.nextPage();
  }

  prevPage(): void {
    this.paginationService.prevPage();
  }
}
