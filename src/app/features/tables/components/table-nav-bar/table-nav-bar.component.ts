import { Component, EventEmitter, inject, Output, OnInit, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TablesResponse } from '../../../../models/tables/table_response';
import { Table } from '../../../../models/tables/table';
import { TableService } from '../../../../services/table.service';
import { TableCardComponent } from '../table-card-name/table-card-name.component';

@Component({
  selector: 'app-table-nav-bar',
  standalone: true,
  imports: [TableCardComponent],
  templateUrl: './table-nav-bar.component.html',
  styleUrl: './table-nav-bar.component.scss'
})
export class TableNavBarComponent implements OnInit {
  private readonly tableService = inject(TableService);
  tables$: Observable<TablesResponse> = new BehaviorSubject<TablesResponse>({});

  tables?: Table[];
  currentPage: number = 1;
  tablesPerPage: number = 9;
  totalPages: number = 1;

  @Output() tableSelected: EventEmitter<Table> = new EventEmitter<Table>();

  ngOnInit() {
    this.updateTablesPerPage();
    this.tables$ = this.tableService.getTables();
    this.tables$.subscribe((data: TablesResponse) => {
      this.tables = Object.entries(data).map(([name, columns]) => ({
        name,
        columns,
      }));
      this.totalPages = Math.ceil(this.tables.length / this.tablesPerPage);
    });
  }

  updateTablesPerPage() {
    const width = window.innerWidth;
    if (width < 640) {
      this.tablesPerPage = 3;
    } else if (width < 768) {
      this.tablesPerPage = 6;
    } else {
      this.tablesPerPage = 8;
    }
    this.totalPages = Math.ceil((this.tables?.length || 0) / this.tablesPerPage); // ceil pour arrondir
    this.currentPage = 1;
  }

  get currentTables(): Table[] {
    const startIndex = (this.currentPage - 1) * this.tablesPerPage;
    let endIndex = startIndex + this.tablesPerPage;

    if (this.tables && endIndex > this.tables.length) {
      const missingCount = endIndex - this.tables.length;
      return this.tables.slice(startIndex - missingCount, this.tables.length);
    }

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

  onTableClick(table: Table): void {
    this.tableSelected.emit(table);
  }
}
