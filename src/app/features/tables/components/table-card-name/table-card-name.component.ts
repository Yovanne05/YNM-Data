import { Component, Input } from '@angular/core';
import { Table } from '../../../../models/table';

@Component({
  selector: 'app-table-card',
  standalone: true,
  imports: [],
  templateUrl: './table-card-name.component.html',
  styleUrl: './table-card-name.component.scss'
})
export class TableCardComponent {
  @Input({ required: true }) name!: String;
}
