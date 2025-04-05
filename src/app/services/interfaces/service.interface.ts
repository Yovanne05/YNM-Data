import { Observable } from "rxjs";
import { TableStructure } from "../../models/transactionnal/table_response";

export interface GenericTableInterface {
  getTableData(
    tableName: string,
    filters?: { [key: string]: { operator: string, value: string } }
  ): Observable<Record<string, string>[]>;
  getTables(): Observable<TableStructure>;
  getTableDataByTableName(table_name: string): Observable<TableStructure>;
  deleteItem(tableName: string, item: any): Observable<any>;
  updateItem(tableName: string, item: any, updatedData: any): Observable<any>;
  getTableSchema(tableName: string): Observable<{[key: string]: string}>;
}
