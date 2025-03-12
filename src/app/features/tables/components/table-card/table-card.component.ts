import { Component, Input } from '@angular/core';
import { Table } from '../../../../models/table';
import { DatabaseService } from '../../../../services/table.service';

@Component({
  selector: 'app-table-card',
  standalone: true,
  imports: [],
  templateUrl: './table-card.component.html',
  styleUrl: './table-card.component.scss'
})
export class TableCardComponent {
  @Input({ required: true }) table!: Table;
}
