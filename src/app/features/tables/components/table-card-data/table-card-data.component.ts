import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { getObjectKeys, getValue } from '../../../../utils/json.method';
import { FilterRegistryService } from '../../../../services/filter.registry.service';
import { FilterManagerService } from '../../../../services/filter.manager.service';
import { GenericTableService } from '../../../../services/generic.service';
import { ApiService } from '../../../../services/delete.edit.service.service';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
  imports: [FormsModule] // Ajout de FormsModule pour ngModel
})
export class TableCardDataComponent implements OnInit, OnChanges {
  private readonly genericTableService = inject(GenericTableService);
  private readonly filterRegistry = inject(FilterRegistryService);
  private readonly filterManager = inject(FilterManagerService);
  private readonly apiService = inject(ApiService);

  @Input() tableName!: string;

  // Données
  tablesData$!: Observable<Record<string, string>[]>;
  tablesData: Record<string, string>[] | null = null;
  filteredData: Record<string, string>[] | null = null;

  // Filtres et tri
  activeFilters: { [key: string]: boolean } = {};
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;
  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];

  // État d'édition
  editingItem: Record<string, string> | null = null;
  tempItem: Record<string, string> = {};
  actionMenuOpen: number | null = null;

  // Dictionnaire des clés primaires
  tablePrimaryKeys: Record<string, string> = {
    utilisateur: 'idUtilisateur',
    abonnement: 'idAbonnement',
    temps: 'idDate',
    genre: 'idGenre',
    titre: 'idTitre',
    serie: 'idSerie',
    film: 'idFilm',
    langue: 'idLangue',
    langue_Disponible: 'idLangueDispo',
    visionnage: 'idVisionnage',
    evaluation: 'idEvaluation',
    paiement: 'idPaiement',
  };

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
    this.actionMenuOpen = null;
    this.cancelEditing();
  }

  private loadData(): void {
    this.tablesData$ = this.genericTableService.getTableData(this.tableName);

    this.tablesData$.subscribe({
      next: (data) => {
        if (data) {
          this.tablesData = data;
          this.availableFilters = this.getAvailableFilters();
          this.applyFiltersAndSort();
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

  // Méthodes d'édition
  startEditing(item: Record<string, string>): void {
    this.editingItem = item;
    this.tempItem = { ...item };
    this.actionMenuOpen = null;
  }

  saveChanges(): void {
    if (!this.editingItem || !this.filteredData) return;

    const primaryKey = this.tablePrimaryKeys[this.tableName];
    if (!primaryKey) {
      console.error(`Colonne d'identifiant non trouvée pour la table ${this.tableName}`);
      return;
    }

    this.apiService.updateItem(this.tableName, this.editingItem[primaryKey], this.tempItem)
      .subscribe({
        next: (response) => {
          // Mise à jour locale
          const index = this.filteredData!.findIndex(i => i[primaryKey] === this.editingItem![primaryKey]);
          if (index !== -1) {
            this.filteredData![index] = { ...this.tempItem };
          }
          this.cancelEditing();
        },
        error: (err) => console.error('Erreur lors de la modification:', err)
      });
  }

  cancelEditing(): void {
    this.editingItem = null;
    this.tempItem = {};
  }

  // Méthodes existantes
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

  toggleActionMenu(index: number): void {
    this.actionMenuOpen = this.actionMenuOpen === index ? null : index;
  }

  onDelete(item: Record<string, string>): void {
    const primaryKey = this.tablePrimaryKeys[this.tableName];
    if (!primaryKey) {
      console.error(`Colonne d'identifiant non trouvée pour la table ${this.tableName}`);
      return;
    }

    this.apiService.deleteItem(this.tableName, item[primaryKey]).subscribe({
      next: (response) => {
        console.log('Élément supprimé:', response);
        this.loadData();
      },
      error: (err) => console.error('Erreur lors de la suppression:', err),
    });
    this.actionMenuOpen = null;
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return getObjectKeys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return getValue(key, item);
  }
}