import { Injectable } from "@angular/core";

@Injectable()
export class TablePaginationService {
  currentPage: number = 1;
  itemsPerPage: number = 15;
  totalItems: number = 0;
  totalPages: number = 1;
  filteredData: any[] = [];
  paginationData: any[] = [];

  setData(data: any[], total?: number, pages?: number): void {
    this.filteredData = data || [];
    this.paginationData = [...this.filteredData];
    this.totalItems = total ?? data?.length ?? 0;
    this.totalPages = pages ?? Math.ceil(this.totalItems / this.itemsPerPage);
  }

  setOnlyData(data: any[]): void {
    this.filteredData = data || [];
    this.paginationData = [...this.filteredData];
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
}
