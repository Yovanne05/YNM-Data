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
import {
  FormsModule,
  ReactiveFormsModule,
  FormGroup,
  FormControl,
} from '@angular/forms';

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
  @Output() sendTablesData = new EventEmitter<
    Record<string, string>[] | null
  >();

  tablesData$!: Observable<Record<string, string>[]>;
  filteredData: Record<string, string>[] | null = null;

  // Filtres et tri
  availableFilters: { key: string; name: string }[] = [];
  showFilters = false;
  filterForm: FormGroup = new FormGroup({});
  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];

  // État d'édition
  editingItem: Record<string, string> | null = null;
  tempItem: Record<string, string> = {};
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
    this.filteredData = null;
    this.actionMenuOpen = null;
    this.sortKeys = [];
    this.filterForm.reset();
    this.cancelEditing();
  }

  private loadData(): void {
    const activeFilters = this.getActiveFilters();
    this.tablesData$ = this.genericTableService.getTableData(
      this.tableName,
      activeFilters
    );

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
      Object.entries(this.filterForm.value)
        .filter(([_, value]) => value)
        .map(([key, value]) => [key, value as string])
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

  
  startEditing(item: Record<string, string>): void {
    this.editingItem = item;
    this.tempItem = { ...item };
    this.actionMenuOpen = null;
  }

  saveChanges(): void {
    if (!this.editingItem || !this.filteredData) return;
    const updatedData = { ...this.tempItem };
    this.genericTableService.updateItem(
        this.tableName,
        this.editingItem,
        updatedData
    ).subscribe({
        next: () => {
            this.loadData();
            this.cancelEditing();
        },
        error: (err) => {
            console.error('Erreur complète:', err);
            alert(`Erreur lors de la modification: ${err.error?.error || err.message}`);
        }
    });
}

  cancelEditing(): void {
    this.editingItem = null;
    this.tempItem = {};
  }

  onSort(key: string): void {
    const existingSortKey = this.sortKeys.find((sort) => sort.key === key);

    if (existingSortKey) {
      existingSortKey.direction =
        existingSortKey.direction === 'asc' ? 'desc' : 'asc';
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

  toggleActionMenu(index: number): void {
    this.actionMenuOpen = this.actionMenuOpen === index ? null : index;
  }

  onDelete(item: Record<string, string>): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
      this.genericTableService.deleteItem(this.tableName, item).subscribe({
        next: () => {
          this.loadData();
        },
        error: (err) => {
          console.error('Erreur lors de la suppression:', err);
          this.loadData();
        },
      });
    }
    this.actionMenuOpen = null;
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return getObjectKeys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return getValue(key, item);
  }


// Propriétés à ajouter
isAddingMode = false;
newItem: {[key: string]: any} = {};
requiredFields: string[] = [];
errorMessage: string | null = null;

// Méthodes à ajouter
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
      this.loadData(); // Recharge les données
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

cancelAdding(): void {
  this.isAddingMode = false;
  this.newItem = {};
  this.errorMessage = null;
}
}
