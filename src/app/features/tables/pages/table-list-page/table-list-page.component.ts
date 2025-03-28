import { Component } from '@angular/core';
import { TableNavBarComponent } from "../../components/table-nav-bar/table-nav-bar.component";
import { TableCardInfoComponent } from "../../components/table-card-info/table-card-info.component";
import { ExportDataComponent } from '../../components/export-data/export-data.component';
import { ImportDataComponent } from '../../components/import-data/import-data.component';

@Component({
  selector: 'app-table-list-page',
  standalone: true,
  imports: [TableNavBarComponent, TableCardInfoComponent, ExportDataComponent, ImportDataComponent],
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
  }
}
