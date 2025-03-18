import { Component, inject, Input, OnInit } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { ServiceFactory } from '../../../../services/service-factory';
import { Utilisateur } from '../../../../models/utilisateur';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss']
})
export class TableCardDataComponent<T> implements OnInit {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$: Observable<T> = new BehaviorSubject<T>({} as T);
  tablesData?: T;

  @Input({ required: true }) tableName!: string;

  ngOnInit() {
    const service = this.serviceFactory.getService(this.tableName);

    if (service) {
      this.tablesData$ = service.getTableData() as Observable<Utilisateur>;

      this.tablesData$.subscribe((data: T) => {
        if (data) {
          if (Array.isArray(data)) {
            this.tablesData = data;
          } else if (typeof data === 'object') {
            this.tablesData = Object.entries(data).map(([key, value]) => ({
              name: key,
              columns: value,
            })) as T;
          } else {
            this.tablesData = data;
          }
        }
      });
    } else {
      console.error('Aucun service ou modèle trouvé pour cette table:', this.tableName);
    }
  }
}
