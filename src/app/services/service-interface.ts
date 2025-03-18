import { Observable } from "rxjs";

export interface Service {
    getTableData(): Observable<any>;
  }