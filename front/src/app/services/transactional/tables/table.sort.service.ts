import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class TableSortService {
  private _sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];

  onSort(key: string): void {
    let newSortKeys = [...this._sortKeys];
    const existingIndex = newSortKeys.findIndex(s => s.key === key);

    if (existingIndex >= 0) {
      const currentDirection = newSortKeys[existingIndex].direction;
      if (currentDirection === 'asc') {
        newSortKeys[existingIndex].direction = 'desc';
      } else {
        newSortKeys.splice(existingIndex, 1);
      }
    } else {
      newSortKeys.push({ key, direction: 'asc' });
    }

    if (newSortKeys.length > 3) {
      newSortKeys = newSortKeys.slice(-3);
    }

    this._sortKeys = newSortKeys;
    console.log(this.sortKeys);
  }


  get sortKeys(): { key: string; direction: "asc" | "desc" }[] {
    return this._sortKeys;
  }
}
