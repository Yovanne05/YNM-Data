import { Component } from '@angular/core';
import { TableNavBarComponent } from "../../components/table-nav-bar/table-nav-bar.component";
import { Table } from '../../../../models/tables/table';
import { TableCardInfoComponent } from "../../components/table-card-info/table-card-info.component";

@Component({
  selector: 'app-table-list-page',
  standalone: true,
  imports: [TableNavBarComponent, TableCardInfoComponent],
  templateUrl: './table-list-page.component.html',
  styleUrl: './table-list-page.component.scss',
})
export class TableListPageComponent{
  selectedTable: Table | null = null;

  handleTableSelection(selectedTable: Table): void {
    this.selectedTable = selectedTable;
  }
}
