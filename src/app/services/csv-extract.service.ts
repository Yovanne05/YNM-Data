import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CsvExtractService {

  exportToCsv(filename: string, data: Record<string, string>[]): void {
    if (!data || data.length === 0) {
      console.warn('Aucune donnée à exporter');
      return;
    }

    // 1. Extraire les en-têtes (clés du premier objet)
    const headers = Object.keys(data[0]).join(',');

    // 2. Extraire les lignes de données
    const rows = data.map(row => 
      Object.values(row)
        .map(value => `"${String(value).replace(/"/g, '""')}"`) // Convertit tout en string
        .join(',')
    );

    // 3. Construire le CSV
    const csvContent = [headers, ...rows].join('\n');

    // 4. Créer un blob et déclencher le téléchargement
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
