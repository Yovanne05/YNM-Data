import { Injectable } from '@angular/core';

@Injectable()
export class TableSortService {
  sortKeys: { key: string; direction: 'asc' | 'desc' }[] = [];

  getSortKeys() {
    return [...this.sortKeys];
  }

  onSort(key: string): void {
    let newSortKeys = [...this.sortKeys];
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

    this.sortKeys = newSortKeys;
  }

  removeSort(key: string): void {
    this.sortKeys = this.sortKeys.filter((s) => s.key !== key);
  }

  clearAllSorts(): void {
    this.sortKeys = [];
  }

  applySort(data: any[]): any[] {
    if (!data || this.sortKeys.length === 0) return data;

    return [...data].sort((a, b) => {
      for (const sort of this.sortKeys) {
        const result = this.compareValues(a[sort.key], b[sort.key], sort.direction);
        if (result !== 0) return result;
      }
      return 0;
    });
  }

  private compareValues(a: any, b: any, direction: 'asc' | 'desc'): number {
    if (a == null || b == null) {
      if (a == null && b == null) return 0;
      return a == null ? (direction === 'asc' ? -1 : 1) : (direction === 'asc' ? 1 : -1);
    }

    const numA = Number(a);
    const numB = Number(b);
    if (!isNaN(numA) && !isNaN(numB)) {
      return direction === 'asc' ? numA - numB : numB - numA;
    }

    const dateA = new Date(a);
    const dateB = new Date(b);
    if (!isNaN(dateA.getTime()) && !isNaN(dateB.getTime())) {
      return direction === 'asc' ? dateA.getTime() - dateB.getTime() : dateB.getTime() - dateA.getTime();
    }

    return direction === 'asc' ? String(a).localeCompare(String(b)) : String(b).localeCompare(String(a));
  }

  getSortDirection(key: string): 'asc' | 'desc' | null {
    const sort = this.sortKeys.find(s => s.key === key);
    return sort ? sort.direction : null;
  }

  getSortOrder(key: string): number | null {
    const index = this.sortKeys.findIndex(s => s.key === key);
    return index !== -1 ? index + 1 : null;
  }

}
