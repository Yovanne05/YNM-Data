import { Observable } from "rxjs";
import { ServiceInterface } from "./service-interface";

export class SerieService implements ServiceInterface{
    getTableData(): Observable<any> {
        throw new Error("Method not implemented.");
    }

}