export interface TableMetadata {
    is_composite: boolean;
    columns: Array<{
      name: string;
      type: string;
    }>;
  }