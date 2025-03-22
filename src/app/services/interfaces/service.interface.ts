import { Observable } from "rxjs";
export interface ServiceInterface {
  getTableData(): Observable<Record<string, string>>;
}
