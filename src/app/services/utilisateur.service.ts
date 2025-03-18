import { Injectable } from "@angular/core";
import { API_CONFIG } from '../config/api.config';
import { HttpClient } from "@angular/common/http";
import { catchError, Observable } from "rxjs";
import { Utilisateur } from "../models/utilisateur";
import { Service } from "./service-interface";

@Injectable({
    providedIn: 'root',
})

export class UtilisateurService implements Service{
    private apiUrl = API_CONFIG.API_URL + '/utilisateur';

    constructor(private readonly http: HttpClient) { }

    getTableData(): Observable<Utilisateur> {
        return this.http.get<Utilisateur>(this.apiUrl).pipe(
            catchError((err) => {
                console.error('Erreur lors de la récupération des utilisateurs', err);
                throw new Error('Une erreur est survenue:', err);
            })
        )
    }
}