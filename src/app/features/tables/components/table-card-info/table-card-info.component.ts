import { TableService } from './../../../../services/table.service';
import { Component, inject, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { Table } from '../../../../models/tables/table';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { BehaviorSubject, Observable } from 'rxjs';
import { TablesResponse } from '../../../../models/tables/table_response';

@Component({
  selector: 'app-table-card-info',
  standalone: true,
  imports: [TableCardDataComponent],
  templateUrl: './table-card-info.component.html',
  styleUrls: ['./table-card-info.component.scss'],
})
export class TableCardInfoComponent implements OnInit, OnChanges {

  @Input({ required: true }) tableName!: string;

  private readonly tableService = inject(TableService);
  table$: Observable<TablesResponse> = new BehaviorSubject<TablesResponse>({});
  table?: Table;

  ngOnInit(): void {
    this.loadTableData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['tableName']) {
      this.loadTableData();
    }
  }

  private loadTableData(): void {
    this.table$ = this.tableService.getTableDataByTableName(this.tableName);
    this.table$.subscribe((data: TablesResponse) => {
      const firstTable = Object.entries(data)[0];
      if (firstTable) {
        const [name, columns] = firstTable;
        this.table = { name, columns };
      }
    });
  }
}
