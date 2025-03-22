import { Observable } from "rxjs";
import { TablesResponse } from "../../models/table_response";
export interface GenericTableInterface {
  getTableData(tableName: string): Observable<Record<string, string> []>;
  getTables(): Observable<TablesResponse>;
  getTableDataByTableName(table_name: string): Observable<TablesResponse>;
}
