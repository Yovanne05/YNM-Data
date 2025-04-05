export interface Table {
  name: string;
  columns: string[];
  data?: Record<string, string>[];
}
