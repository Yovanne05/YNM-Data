import { Component, inject } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TablesResponse } from '../../../../models/table_response';
import { Table } from '../../../../models/table';
import { DatabaseService } from '../../../../services/table.service';
import { TableCardComponent } from '../table-card/table-card.component';

@Component({
  selector: 'app-table-nav-bar',
  standalone: true,
  imports: [TableCardComponent],
  templateUrl: './table-nav-bar.component.html',
  styleUrl: './table-nav-bar.component.scss'
})
export class TableNavBarComponent {
 private readonly dbService = inject(DatabaseService);
  tables$: Observable<TablesResponse> = new BehaviorSubject<TablesResponse>({});
  tables?: Table[];
  currentPage: number = 1;
  tablesPerPage: number = 5;
  totalPages: number = 1;

  ngOnInit() {
    this.tables$ = this.dbService.getTables();
    this.tables$.subscribe((data: TablesResponse) => {
      this.tables = Object.entries(data).map(([name, columns]) => ({
        name,
        columns,
      }));
      this.totalPages = Math.ceil(this.tables.length / this.tablesPerPage);
    });
  }

  get currentTables(): Table[] {
    const startIndex = (this.currentPage - 1) * this.tablesPerPage;
    const endIndex = startIndex + this.tablesPerPage;
    return this.tables?.slice(startIndex, endIndex) || [];
  }

  goToNextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  goToPreviousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
}
