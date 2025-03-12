import { Component, inject, OnInit } from '@angular/core';
import { Table } from '../../../../models/table';
import { DatabaseService } from '../../../../services/table.service';
import { TablesResponse } from '../../../../models/table_response';
import { TableCardComponent } from '../../components/table-card/table-card.component';
import { BehaviorSubject, Observable } from 'rxjs';

@Component({
  selector: 'app-table-list-page',
  standalone: true,
  imports: [TableCardComponent],
  templateUrl: './table-list-page.component.html',
  styleUrl: './table-list-page.component.scss',
})

export class TableListPageComponent implements OnInit {
  private readonly dbService = inject(DatabaseService);
  tables$: Observable<TablesResponse> = new BehaviorSubject<TablesResponse>({});
  tables?: Table[];

  ngOnInit() {
    this.tables$ = this.dbService.getTables();
    this.tables$.subscribe((data: TablesResponse) => {
      this.tables = Object.entries(data).map(([name, columns]) => ({
        name,
        columns,
      }));
    });
  }
}
