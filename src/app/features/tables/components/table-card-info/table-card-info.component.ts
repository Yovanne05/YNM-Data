import { Component, Input } from '@angular/core';
import { Table } from '../../../../models/tables/table';
import { TableCardDataComponent } from "../table-card-data/table-card-data.component";

@Component({
  selector: 'app-table-card-info',
  standalone: true,
  imports: [TableCardDataComponent],
  templateUrl: './table-card-info.component.html',
  styleUrl: './table-card-info.component.scss'
})
export class TableCardInfoComponent {
@Input({required: true}) table!: Table;
}
