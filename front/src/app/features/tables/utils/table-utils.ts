export function isIdColumn(column: string, tableName: string): boolean {
  if (!column) return false;
  const lowerColumn = column.toLowerCase();
  return lowerColumn === 'id' ||
    lowerColumn === `id${tableName.charAt(0).toUpperCase() + tableName.slice(1)}`.toLowerCase();
}

export function getUserFriendlyError(err: any): string {
  if (err.message.includes('Impossible de se connecter au serveur')) {
    return 'Serveur indisponible. Veuillez vérifier votre connexion.';
  }
  if (err.message.includes('Erreur serveur')) {
    return 'Le serveur a rencontré une erreur. Détails techniques: ' + err.message;
  }
  return err.message || 'Erreur lors de la création';
}
