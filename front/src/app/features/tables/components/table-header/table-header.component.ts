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

  getSortDirection(column: string): 'asc' | 'desc' | null {
    const sortKey = this.sortKeys.find(s => s.key === column);
    return sortKey ? sortKey.direction : null;
  }

  getSortOrder(column: string): number | null {
    const index = this.sortKeys.findIndex(s => s.key === column);
    return index >= 0 ? index + 1 : null;
  }

  onSort(key: string) {
    this.sort.emit(key);
  }
}
