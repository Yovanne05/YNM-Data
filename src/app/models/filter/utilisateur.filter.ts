import { FilterStrategy } from "../interface/filter.interface";
import { UtilisateurService } from "../../services/utilisateur.service";

export class StatutAbonnementFilter implements FilterStrategy {
    filter(param: string | Record<string, string>[], criteria: any): Record<string, string>[] {
        let data: Record<string, string>[];

        if (typeof param === "string") {
            data = this.getDataFromTable(param);
        } else {
            data = param;
        }

        const filteredData = data.filter(item =>
            item['statutAbonnement'] === "Actif"
        );

        return filteredData;
    }

    private getDataFromTable(tableName: string): Record<string, string>[] {
        // méthode service a faire
        console.log(`Fetching data for table: ${tableName}`);
        return [];
    }
}
