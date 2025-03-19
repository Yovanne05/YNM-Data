import { Observable } from "rxjs";

export interface ServiceInterface<T> {
    getTableData(): Observable<T>;
  }
