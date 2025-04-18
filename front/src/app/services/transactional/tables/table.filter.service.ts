import { Injectable } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class TableFilterService {
  filterForm: FormGroup = new FormGroup({});

  initFilterForm(filters: any[]): void {
    const controls: Record<string, FormControl> = {};

    filters?.forEach((filter) => {
      const key = filter['key'];
      const type = filter['type'];

      if (!key) return;

      controls[key] = new FormControl('');

      if (type === 'number') {
        controls[`${key}_operator`] = new FormControl('eq');
      }
    });

    this.filterForm = new FormGroup(controls);
  }

  getActiveFilters(): { [key: string]: { operator: string; value: any } } {
    const filters: { [key: string]: { operator: string; value: any } } = {};

    Object.keys(this.filterForm.controls).forEach((key) => {
      if (key.endsWith('_operator')) return;

      const value = this.filterForm.get(key)?.value;
      if (value !== null && value !== undefined && value !== '') {
        const operatorControl = this.filterForm.get(`${key}_operator`);
        filters[key] = {
          operator: operatorControl?.value || 'eq',
          value: value
        };
      }
    });

    return filters;
  }

  resetFilters(): void {
    this.filterForm.reset();
  }
}
