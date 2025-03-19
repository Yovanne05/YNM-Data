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
  styleUrls: ['./table-nav-bar.component.scss']
})
export class TableNavBarComponent implements OnInit {
  private readonly tableService = inject(TableService);
  tables$: Observable<TablesResponse> = new BehaviorSubject<TablesResponse>({});

  tableNames: string[] = [];
  currentPage: number = 1;
  tablesPerPage: number = 9;
  totalPages: number = 1;

  @Output() tableSelected: EventEmitter<string> = new EventEmitter<string>();

  ngOnInit() {
    this.updateTablesPerPage();
    this.tables$ = this.tableService.getTables();
    this.tables$.subscribe((data: TablesResponse) => {
      this.tableNames = Object.keys(data);
      this.totalPages = Math.ceil(this.tableNames.length / this.tablesPerPage);
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
    this.totalPages = Math.ceil(this.tableNames.length / this.tablesPerPage);
    this.currentPage = 1;
  }

  get currentTables(): string[] {
    const startIndex = (this.currentPage - 1) * this.tablesPerPage;
    let endIndex = startIndex + this.tablesPerPage;

    if (endIndex > this.tableNames.length) {
      const missingCount = endIndex - this.tableNames.length;
      return this.tableNames.slice(startIndex - missingCount, this.tableNames.length);
    }

    return this.tableNames.slice(startIndex, endIndex);
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

  onTableClick(tableName: string): void {
    this.tableSelected.emit(tableName);
  }
}
