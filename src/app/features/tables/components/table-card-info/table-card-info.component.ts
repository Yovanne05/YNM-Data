import { Component, inject, Input, OnInit, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { Table } from '../../../../models/table';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { BehaviorSubject, Observable } from 'rxjs';
import { TablesResponse } from '../../../../models/table_response';
import { GenericTableService } from '../../../../services/generic.service';

@Component({
  selector: 'app-table-card-info',
  standalone: true,
  imports: [TableCardDataComponent],
  templateUrl: './table-card-info.component.html',
  styleUrls: ['./table-card-info.component.scss'],
})
export class TableCardInfoComponent implements OnInit, OnChanges {

  @Input({ required: true }) tableName!: string;

  @Output() sendTablesData = new EventEmitter<Record<string, string>[] | null>

  private readonly genericTableService = inject(GenericTableService);
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
    this.table$ = this.genericTableService.getTableDataByTableName(this.tableName);
    this.table$.subscribe((data: TablesResponse) => {
      const firstTable = Object.entries(data)[0];
      if (firstTable) {
        const [name, columns] = firstTable;
        this.table = { name, columns };
      }
    });
  }

  emitTablesData(data: Record<string, string>[] | null): void {
    this.sendTablesData.emit(data);
  }
}
