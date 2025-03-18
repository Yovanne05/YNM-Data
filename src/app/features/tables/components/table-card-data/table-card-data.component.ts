import { Component, inject, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ServiceFactory } from '../../../../services/service-factory';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss'],
})
export class TableCardDataComponent<T> implements OnInit {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$!: Observable<T>;
  tablesData?: T;

  @Input() tableName!: string;

  ngOnInit(): void {
    const service = this.serviceFactory.getService(this.tableName);

    if (service) {
      this.tablesData$ = service.getTableData() as Observable<T>;
      this.tablesData$.subscribe({
        next: (data: T) => { // next pr être appeller a chaque fois que l'obeservable chang
          console.log('tablesData$', data);
          if (data) {
            this.tablesData = data;
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
}
