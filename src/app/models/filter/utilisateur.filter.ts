import { BaseFilter } from "./base.filter";
export class StatutAbonnementFilter extends BaseFilter {
    filter(data: Record<string, string>[]): Record<string, string>[] {
        const filteredData = data.filter(item =>
            item['statutAbonnement'] === "Actif"
        );
        return filteredData;
    }
}
