import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CsvExtractService {

  //TODO: Essayer de refaire sans ChatGPT plus tard

  exportToCsv(filename: string, data: Record<string, string>[]): void {

    const headers = Object.keys(data[0]).join(',');

    const rows = data.map(row => 
      Object.values(row)
        .map(value => `"${String(value).replace(/"/g, '""')}"`)
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
