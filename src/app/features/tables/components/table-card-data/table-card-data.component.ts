import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { getObjectKeys, getValue } from '../../../../utils/json.method';
import { FilterRegistryService } from '../../../../services/filter.registry.service';
import { FilterManagerService } from '../../../../services/filter.manager.service';
import { GenericTableService } from '../../../../services/generic.service';
import { ApiService } from '../../../../services/delete.edit.service.service'; // Importez le service ApiService

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
  private readonly apiService = inject(ApiService); // Injectez le service ApiService

  @Input() tableName!: string;

  tablesData$!: Observable<Record<string, string>[]>;
  tablesData: Record<string, string>[] | null = null;
  filteredData: Record<string, string>[] | null = null;

  activeFilters: { [key: string]: boolean } = {};
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;

  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];
  actionMenuOpen: number | null = null;

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

  tablePrimaryKeys: Record<string, string> = {
    utilisateur: 'idUtilisateur',
    Abonnement: 'idAbonnement',
    Temps: 'idDate',
    Genre: 'idGenre',
    Titre: 'idTitre',
    Serie: 'idSerie',
    Film: 'idFilm',
    Langue: 'idLangue',
    Langue_Disponible: 'idLangueDispo',
    Visionnage: 'idVisionnage',
    Evaluation: 'idEvaluation',
    Paiement: 'idPaiement',
  };

  onEdit(item: Record<string, string>): void {
    // Récupérer la colonne d'identifiant pour la table actuelle
    const primaryKey = this.tablePrimaryKeys[this.tableName];
    if (!primaryKey) {
      console.error(`Colonne d'identifiant non trouvée pour la table ${this.tableName}`);
      return;
    }
  
    // Exemple de logique pour modifier un élément
    const updatedData = { ...item, name: 'Nouveau nom' }; // Remplacez par les nouvelles données
    this.apiService.updateItem(this.tableName, item[primaryKey], updatedData).subscribe({
      next: (response) => {
        console.log('Élément modifié:', response);
        this.loadData(); // Recharger les données après modification
      },
      error: (err) => console.error('Erreur lors de la modification:', err),
    });
    this.actionMenuOpen = null;
  }

  onDelete(item: Record<string, string>): void {
    // Récupérer la colonne d'identifiant pour la table actuelle
    const primaryKey = this.tablePrimaryKeys[this.tableName];
    if (!primaryKey) {
      console.error(`Colonne d'identifiant non trouvée pour la table ${this.tableName}`);
      return;
    }
  
    // Exemple de logique pour supprimer un élément
    this.apiService.deleteItem(this.tableName, item[primaryKey]).subscribe({
      next: (response) => {
        console.log('Élément supprimé:', response);
        this.loadData(); // Recharger les données après suppression
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