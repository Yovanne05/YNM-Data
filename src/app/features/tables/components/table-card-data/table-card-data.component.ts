import { Component, EventEmitter, Input, OnChanges, SimpleChanges, inject, output, OnDestroy } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { TableFiltersComponent } from '../table-filters/table-filters.component';
import { TableHeaderComponent } from '../table-header/table-header.component';
import { TableRowComponent } from '../table-row/table-row.component';
import { FilterRegistryService } from '../../../../services/transactional/filter.registry.service';
import { GenericTableService } from '../../../../services/transactional/generic.service';
import { Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  imports: [ReactiveFormsModule, TableFiltersComponent, TableHeaderComponent, TableRowComponent, CommonModule, FormsModule],
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss']
})
export class TableCardDataComponent implements OnChanges, OnDestroy {
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

  isAddingMode = false;
  newItem: {[key: string]: any} = {};
  requiredFields: string[] = [];
  errorMessage: string | null = null;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data'] && this.data.length > 0) {
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

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  /**
   * Gère le tri multi-colonnes (asc → desc → reset)
   * @param key - La colonne à trier
   */
  onSort(key: string): void {
    let newSortKeys = [...this.sortKeys];
    const existingIndex = newSortKeys.findIndex(s => s.key === key);

    if (existingIndex >= 0) {
      const currentDirection = newSortKeys[existingIndex].direction;
      if (currentDirection === 'asc') {
        newSortKeys[existingIndex].direction = 'desc';
      } else {
        newSortKeys.splice(existingIndex, 1);
      }
    } else {
      newSortKeys.push({ key, direction: 'asc' });
    }

    if (newSortKeys.length > 3) {
      newSortKeys = newSortKeys.slice(-3);
    }

    this.sortKeys = newSortKeys;
    this.applySort();
    this.sortChanged.emit([...this.sortKeys]);
  }

  /**
   * Applique les tris cumulatifs selon la priorité d'ajout
   */
  private applySort(): void {
    if (!this.filteredData || this.sortKeys.length === 0) return;

    this.filteredData = [...this.filteredData].sort((a, b) => {
      for (const sort of this.sortKeys) {
        const result = this.compareValues(a[sort.key], b[sort.key], sort.direction);
        if (result !== 0) return result;
      }
      return 0;
    });
  }

  /**
   * Compare deux valeurs avec détection automatique du type
   * @param a - Première valeur à comparer
   * @param b - Deuxième valeur à comparer
   * @param direction - Direction du tri ('asc' ou 'desc')
   * @returns Résultat de comparaison (-1, 0, 1)
   */
  private compareValues(a: any, b: any, direction: 'asc' | 'desc'): number {
    if (a == null || b == null) {
      if (a == null && b == null) return 0;
      return a == null ? (direction === 'asc' ? -1 : 1) : (direction === 'asc' ? 1 : -1);
    }

    const numA = Number(a);
    const numB = Number(b);
    if (!isNaN(numA) && !isNaN(numB)) {
      return direction === 'asc' ? numA - numB : numB - numA;
    }

    const dateA = new Date(a);
    const dateB = new Date(b);
    if (!isNaN(dateA.getTime()) && !isNaN(dateB.getTime())) {
      return direction === 'asc' ? dateA.getTime() - dateB.getTime() : dateB.getTime() - dateA.getTime();
    }

    return direction === 'asc' ? String(a).localeCompare(String(b)) : String(b).localeCompare(String(a));
  }

  removeSort(key: string): void {
    this.sortKeys = this.sortKeys.filter((s) => s.key !== key);
    this.applySort();
    this.sortChanged.emit(this.sortKeys);
  }

  clearAllSorts(): void {
    this.sortKeys = [];
    this.filteredData = [...this.data];
    this.sortChanged.emit([]);
  }

  private loadFilters(): void {
    this.filterRegistry.getFiltersForTable(this.tableName).subscribe({
      next: (filters) => {
        this.filters = filters;
        this.initFilterForm();
        this.loadDataWithFilters();
      },
      error: (err) => console.error('Error loading filters:', err),
    });
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

  private loadDataWithFilters(): void {
    const activeFilters = this.getActiveFilters();

    this.dataSubscription = this.genericTableService
      .getTableData(this.tableName, activeFilters)
      .subscribe({
        next: (data) => {
          this.filteredData = [...data];
          this.applySort();
          this.sendTablesData.emit([...this.filteredData]);
        },
        error: (err) => console.error('Error loading filtered data:', err),
      });
  }

  private getActiveFilters(): { [key: string]: { operator: string; value: any } } {
    const filters: { [key: string]: { operator: string; value: any } } = {};

    Object.keys(this.filterForm.controls).forEach((key) => {
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
    Object.keys(item).forEach((key) => {
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

  cancelAdding(): void {
    this.isAddingMode = false;
    this.newItem = {};
    this.errorMessage = null;
  }

  saveNewItem(): void {
    // Validation des champs requis
    const missingFields = this.requiredFields.filter(field => !this.newItem[field]);

    if (missingFields.length > 0) {
      this.errorMessage = `Champs requis manquants: ${missingFields.join(', ')}`;
      return;
    }

    // Conversion des types si nécessaire
    this.convertDataTypes();

    this.genericTableService.createItem(this.tableName, this.newItem).subscribe({
      next: (response) => {
        this.loadDataWithFilters(); // Recharge les données
        this.isAddingMode = false;
        this.newItem = {};
      },
      error: (err) => {
        this.errorMessage = err.message;
        console.error('Erreur détaillée:', err);
      }
    });
  }

  private convertDataTypes(): void {
    // Convertit les champs numériques
    const numericFields = ['id', 'age', 'prix', 'annee', 'duree', 'saison'];
    numericFields.forEach(field => {
      if (this.newItem[field] !== undefined) {
        this.newItem[field] = Number(this.newItem[field]);
      }
    });

    // Convertit les champs date
    const dateFields = ['dateDebutLicence', 'dateFinLicence'];
    dateFields.forEach(field => {
      if (this.newItem[field]) {
        this.newItem[field] = new Date(this.newItem[field]).toISOString().split('T')[0];
      }
    });
  }

  startAdding(): void {
    this.isAddingMode = true;
    this.newItem = {};
    this.errorMessage = null;
    this.loadRequiredFields();
    this.cancelEditing(); // Annule l'édition en cours si elle existe
  }

  private loadRequiredFields(): void {
    // Cette méthode devrait idéalement faire un appel API pour récupérer
    // les champs requis depuis le backend. Pour l'exemple, nous utilisons
    // une solution temporaire:

    const requiredFieldsMap: {[key: string]: string[]} = {
      'Utilisateur': ['nom', 'prenom', 'email', 'numero'],
      'Abonnement': ['typeAbonnement', 'prix', 'idUtilisateur'],
      'Titre': ['nom', 'annee', 'dateDebutLicence', 'dateFinLicence']
    };

    this.requiredFields = requiredFieldsMap[this.tableName] || [];
  }

}
