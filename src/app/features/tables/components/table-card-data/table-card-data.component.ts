import { Component, inject, Input, OnInit } from '@angular/core';
import { TableService } from '../../../../services/table.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { TableDataResponse } from '../../../../models/tables/TableDataReponse';

@Component({
  selector: 'app-table-card-data',
  standalone: true,
  imports: [],
  templateUrl: './table-card-data.component.html',
  styleUrl: './table-card-data.component.scss'
})
export class TableCardDataComponent implements OnInit{
  private readonly tableService = inject(TableService);
  tablesData$: Observable<TableDataResponse> = new BehaviorSubject<TableDataResponse>({});
  tablesData?: TableDataResponse[];

  @Input({required: true}) tableName!: string;

   ngOnInit() {
      this.tablesData$ = this.tableService.getTableData(this.tableName);
      this.tablesData$.subscribe((data: TableDataResponse) => {
        this.tablesData = Object.entries(data).map(([name, columns]) => ({
          name,
          columns,
        }));
      });
    }

    
}
