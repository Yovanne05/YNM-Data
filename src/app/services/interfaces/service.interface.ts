import { Observable } from "rxjs";
import { TablesResponse } from "../../models/table_response";
export interface GenericTableInterface {
  getTableData(tableName: string): Observable<Record<string, string> []>;
  getTableData(tableName: string, filters?: { [key: string]: string }): Observable<Record<string, string>[]>
  getTableDataByTableName(table_name: string): Observable<TablesResponse>;
}
