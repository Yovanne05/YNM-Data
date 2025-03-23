import { Component } from '@angular/core';
import { TableNavBarComponent } from "../../components/table-nav-bar/table-nav-bar.component";
import { Table } from '../../../../models/table';
import { TableCardInfoComponent } from "../../components/table-card-info/table-card-info.component";
import { ExportDataComponent } from '../../components/export-data/export-data.component';

@Component({
  selector: 'app-table-list-page',
  standalone: true,
  imports: [TableNavBarComponent, TableCardInfoComponent, ExportDataComponent],
  templateUrl: './table-list-page.component.html',
  styleUrl: './table-list-page.component.scss',
})
export class TableListPageComponent{
  selectedTable: string = 'abonnement';
  tablesData!: Record<string, string>[] | null;

  handleTableSelection(selectedTable: string): void {
    this.selectedTable = selectedTable;
  }

  initTablesData(data: Record<string, string>[] | null): void {
    this.tablesData = data;
    data?.forEach((data) => console.log(data))  
  }
}
