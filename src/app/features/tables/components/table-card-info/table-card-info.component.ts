import { Component, Input } from '@angular/core';
import { Table } from '../../../../models/table';

@Component({
  selector: 'app-table-card-info',
  standalone: true,
  imports: [],
  templateUrl: './table-card-info.component.html',
  styleUrl: './table-card-info.component.scss'
})
export class TableCardInfoComponent {
@Input({required: true}) table!: Table;
}
