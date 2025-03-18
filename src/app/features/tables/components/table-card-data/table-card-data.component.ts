import { Component, inject, Input, OnInit } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TableDataResponse } from '../../../../models/tables/TableDataReponse';
import { ServiceFactory } from '../../../../services/service-factory';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  templateUrl: './table-card-data.component.html',
  styleUrls: ['./table-card-data.component.scss']
})
export class TableCardDataComponent implements OnInit {
  private readonly serviceFactory = inject(ServiceFactory);

  tablesData$: Observable<TableDataResponse> = new BehaviorSubject<TableDataResponse>({});
  tablesData?: TableDataResponse[];

  @Input({ required: true }) tableName!: string;

  ngOnInit() {
    const service = this.serviceFactory.getService(this.tableName);
    if (service) {
      this.tablesData$ = service.getTableData();
      this.tablesData$.subscribe((data: TableDataResponse) => {
        this.tablesData = Object.entries(data).map(([name, columns]) => ({
          name,
          columns,
        }));
      });
    } else {
      console.error('Aucun service trouvé pour cette table:', this.tableName);
    }
  }

}
