import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ServiceFactory } from '../../../../services/service-factory';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent<T> implements OnInit, OnChanges {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$!: Observable<T>;
  tablesData: any;

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
      this.tablesData$ = service.getTableData() as Observable<T>;
      this.tablesData$.subscribe({
        next: (data: T) => {
          console.log('data', data);
          if (data) {
            this.tablesData = data;
            console.log('tablesData', this.tablesData);
          }
        },
        error: (err) => {
          console.error('Erreur de souscription:', err);
        },
      });
    } else {
      console.error(
        'Aucun service ou modèle trouvé pour cette table:',
        this.tableName
      );
    }
  }

  getObjectKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  getValue(key: string, item: any): any {
    return item ? item[key] : null;
  }
}
