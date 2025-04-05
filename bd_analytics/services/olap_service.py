from sqlalchemy import func, and_, or_
from sqlalchemy.sql import label
from databases.db import db
import pandas as pd


class OLAPService:
    def __init__(self, session):
        self.session = session

    def scoping(self, fact_table, dimensions, measures, filters=None, aggregation_funcs=None):
        """
        Scoping: Extraction d'un bloc de données avec plusieurs dimensions et mesures
        Args:
            fact_table: Table de faits
            dimensions: Liste de dimensions
            measures: Liste de mesures
            filters: Dictionnaire de filtres {dimension_attr: value}
            aggregation_funcs: Dictionnaire de fonctions d'agrégation {measure: func}
        Returns:
            DataFrame pandas avec les résultats
        """
        if aggregation_funcs is None:
            aggregation_funcs = {m: func.sum for m in measures}

        select_columns = []
        for dim in dimensions:
            select_columns.append(dim)

        for measure in measures:
            select_columns.append(
                label(f'aggregated_{measure}', aggregation_funcs[measure](getattr(fact_table, measure))))

        query = self.session.query(*select_columns)

        for dim in dimensions:
            if hasattr(fact_table, dim.name.lower()):
                query = query.join(dim)

        if filters:
            filter_conditions = []
            for attr, value in filters.items():
                parts = attr.split('.')
                if len(parts) == 2:
                    table, column = parts
                    filter_conditions.append(getattr(globals()[table], column) == value)
                else:
                    filter_conditions.append(getattr(fact_table, attr) == value)
            query = query.filter(and_(*filter_conditions))

        query = query.group_by(*dimensions)

        results = query.all()

        columns = [d.name for d in dimensions] + [f'aggregated_{m}' for m in measures]
        df = pd.DataFrame(results, columns=columns)

        return df

