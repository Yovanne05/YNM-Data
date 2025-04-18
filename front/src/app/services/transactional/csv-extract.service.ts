import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CsvExtractService {

  exportToCsv(filename: string, data: Record<string, string>[]): void {

    const headers = Object.keys(data[0]).join(',');

    const rows = data.map(row => 
      Object.values(row)
        .map(value => {
          const strValue = String(value);
          if (strValue.includes('GMT')) { 
            return `"${new Date(strValue).toISOString().split("T")[0]}"`;
          }
    
          return `"${strValue.replace(/"/g, '""')}"`;
        })
        .join(',')
    );

    const csvContent = [headers, ...rows].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
