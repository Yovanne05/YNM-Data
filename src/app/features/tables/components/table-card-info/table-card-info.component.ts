import { Component, inject, Input, OnInit, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { Table } from '../../../../models/transactionnal/table';
import { TableCardDataComponent } from '../table-card-data/table-card-data.component';
import { BehaviorSubject, Observable } from 'rxjs';
import { TableStructure } from '../../../../models/transactionnal/table_response';
import { GenericTableService } from '../../../../services/transactional/generic.service';

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
  table$: Observable<TableStructure> = new BehaviorSubject<TableStructure>({});
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

    this.table$.subscribe({
      next: (data: TableStructure) => {
        const firstTable = Object.entries(data)[0];
        if (firstTable) {
          const [name, columns] = firstTable;

          this.genericTableService.getTableData(this.tableName).subscribe({
            next: (response) => {
              this.table = {
                name,
                columns,
                data: response.items,
                pagination: {
                  total: response.total,
                  page: response.page,
                  pages: response.pages
                }
              };
              this.emitTablesData(this.table.data);
            },
            error: (err) => {
              console.error('Erreur lors du chargement des données:', err);
              this.table = {
                name,
                columns,
                data: [],
                pagination: {
                  total: 0,
                  page: 1,
                  pages: 1
                }
              };
            }
          });
        }
      },
      error: (err) => console.error('Erreur lors du chargement de la table:', err)
    });
  }

  emitTablesData(data: Record<string, string>[] | undefined): void {
    this.sendTablesData.emit(data);
  }
}
