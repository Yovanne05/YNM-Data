import { Component, inject, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ServiceFactory } from '../../../../services/service-factory';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent implements OnInit, OnChanges {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$!: Observable<Record<string, unknown>[]>;
  tablesData: Record<string, unknown>[] | null = null;

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
      this.tablesData$ = service.getTableData() as unknown as Observable<Record<string, unknown>[]>;
      this.tablesData$.subscribe({
        next: (data: Record<string, unknown>[]) => {
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
        'Aucun service trouvé pour cette table:',
        this.tableName
      );
    }
  }

  getObjectKeys(obj: Record<string, unknown>): string[] {
    return Object.keys(obj);
  }

  getValue(key: string, item: Record<string, unknown>): unknown {
    return item ? item[key] : null;
  }
}
