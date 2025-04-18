import { Injectable } from '@angular/core';
import { GenericTableService } from './generic.service';
import { catchError, map, shareReplay } from 'rxjs/operators';
import { Observable, of } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class FilterRegistryService {
  private tableFilters: { [tableName: string]: Observable<any[]> } = {};

  constructor(private genericTableService: GenericTableService) {}

  getFiltersForTable(tableName: string): Observable<any[]> {
    if (!this.tableFilters[tableName]) {
      this.tableFilters[tableName] = this.genericTableService.getTableSchema(tableName).pipe(
        map(schema => {
          const filters = this.generateFiltersFromSchema(schema);
          return filters;
        }),
        catchError(err => {
          console.error('Error in filter generation:', err);
          return of([]);
        }),
        shareReplay(1)
      );
    }
    return this.tableFilters[tableName];
  }

  private generateFiltersFromSchema(schema: {[key: string]: any}): any[] {
    const filters = [];
    const typeMapping: {[key: string]: string} = {
      'varchar': 'text',
      'text': 'text',
      'int': 'number',
      'integer': 'number',
      'decimal': 'number',
      'float': 'number',
      'double': 'number',
      'date': 'date',
      'datetime': 'date',
      'timestamp': 'date',
      'tinyint': 'boolean'
    };

    for (const [column, columnInfo] of Object.entries(schema)) {
      const type = typeof columnInfo === 'string'
        ? columnInfo
        : columnInfo.type || 'text';

      const baseType = type.split('(')[0].toLowerCase();
      const filterType = typeMapping[baseType] || 'text';

      const filterDef: any = {
        key: column,
        label: this.formatLabel(column),
        type: filterType,
      };

      if (filterType === 'number') {
        filterDef.hasOperator = true;
      }

      filters.push(filterDef);
    }

    return filters;
  }

  private formatLabel(column: string): string {
    return column.replace(/_/g, ' ')
                .replace(/([A-Z])/g, ' $1')
                .replace(/^./, str => str.toUpperCase());
  }
}
