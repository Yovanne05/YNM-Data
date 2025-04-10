import { Injectable } from '@angular/core';

@Injectable()
export class TablePaginationService {
  dataPerPage: number = 8;
  filteredData: any[] = [];
  paginationData: any[] = [];
  actualPage: number = 0;
  pageNumber: number = 0;

  setData(data: any[]): void {
    this.filteredData = data;
    this.setPaginationData();
  }

  setPaginationData(): void {
    this.paginationData = this.filteredData.slice(
      this.actualPage * this.dataPerPage,
      (this.actualPage + 1) * this.dataPerPage
    );
    this.pageNumber = Math.ceil(this.filteredData.length / this.dataPerPage);
  }

  nextPage(): void {
    if(this.actualPage + 1 < this.pageNumber) {
      this.actualPage++;
      this.setPaginationData();
    }
  }

  prevPage(): void {
    if(this.actualPage - 1 >= 0) {
      this.actualPage--;
      this.setPaginationData();
    }
  }
}
