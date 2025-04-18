import { Component, EventEmitter, inject, Output, OnInit, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TableStructure } from '../../../../models/transactionnal/table_response';
import { TableCardComponent } from '../table-card-name/table-card-name.component';
import { GenericTableService } from '../../../../services/transactional/generic.service';
import {MatIcon} from "@angular/material/icon";

@Component({
  selector: 'app-table-nav-bar',
  standalone: true,
  imports: [TableCardComponent, MatIcon],
  templateUrl: './table-nav-bar.component.html',
  styleUrls: ['./table-nav-bar.component.scss']
})
export class TableNavBarComponent implements OnInit {
  private readonly genericTableService = inject(GenericTableService);
  tables$: Observable<TableStructure> = new BehaviorSubject<TableStructure>({});

  tableNames: string[] = [];
  currentPage: number = 1;
  tablesPerPage: number = 9;
  totalPages: number = 1;

  @Output() tableSelected: EventEmitter<string> = new EventEmitter<string>();

  ngOnInit() {
    this.updateTablesPerPage();
    this.tables$ = this.genericTableService.getTables();
    this.tables$.subscribe((data: TableStructure) => {
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
      this.tablesPerPage = 11;
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
