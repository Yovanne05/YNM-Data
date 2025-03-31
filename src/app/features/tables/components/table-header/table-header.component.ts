import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-table-header',
  standalone: true,
  templateUrl: './table-header.component.html',
  styleUrls: ['./table-header.component.scss']
})
export class TableHeaderComponent {
  @Input() columns: string[] = [];
  @Input() sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];
  @Output() sort = new EventEmitter<string>();

  onSort(key: string) {
    this.sort.emit(key);
  }
}
