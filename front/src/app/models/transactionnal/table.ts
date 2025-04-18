export interface Table {
  name: string;
  columns: string[];
  data: Record<string, string>[];
  pagination: {
    total: number;
    page: number;
    pages: number;
  };
}
