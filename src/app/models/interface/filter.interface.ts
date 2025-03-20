export interface FilterStrategy {
    filter(tableName: string, criteria: any): Record<string, string>[];
    filter(data: Record<string, string>[], criteria: any): Record<string, string>[];
}
