import { Observable } from "rxjs";
import { ServiceInterface } from "./service-interface";
import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root',
})


export class SerieService implements ServiceInterface{
    getTableData(): Observable<any> {
        throw new Error("Method not implemented.");
    }

}