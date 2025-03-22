export interface FilterStrategy {
    filter(data: Record<string, string>[]): Record<string, string>[];
}
