export interface FilterStrategy {
    filter(tableName: string): Record<string, string>[];
    filter(data: Record<string, string>[]): Record<string, string>[];
}
