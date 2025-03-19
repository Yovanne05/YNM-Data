import { Observable } from "rxjs";
import { ServiceInterface } from "./service-interface";
import { Injectable } from "@angular/core";
import { Utilisateur } from "../models/utilisateur";

@Injectable({
  providedIn: 'root',
})


export class SerieService implements ServiceInterface <Utilisateur>{
    getTableData(): Observable<any> {
        throw new Error("Method not implemented.");
    }

}
