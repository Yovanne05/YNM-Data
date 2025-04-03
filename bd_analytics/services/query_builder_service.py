from sqlalchemy import func, case, and_

class QueryBuilder:
    @staticmethod
    def build_olap_query(session, fact_model, dimensions, measures, filters=None):
        """
        Construit dynamiquement une requête OLAP
        """
        select_columns = []
        for dim in dimensions:
            select_columns.append(getattr(fact_model, dim))

        # Agrégations
        for measure in measures:
            if measure.startswith('count_'):
                col = measure[6:]
                select_columns.append(func.count(getattr(fact_model, col)).label(measure))
            elif measure.startswith('sum_'):
                col = measure[4:]
                select_columns.append(func.sum(getattr(fact_model, col)).label(measure))
            elif measure.startswith('avg_'):
                col = measure[4:]
                select_columns.append(func.avg(getattr(fact_model, col)).label(measure))

        # Construction de la requête
        query = session.query(*select_columns)

        # Jointures
        query = QueryBuilder._add_joins(query, fact_model, dimensions)

        # Filtres
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if '__' in key:  # Filtre sur relation
                    rel, field = key.split('__')
                    filter_conditions.append(getattr(getattr(fact_model, rel), field) == value)
                else:
                    filter_conditions.append(getattr(fact_model, key) == value)
            query = query.filter(and_(*filter_conditions))

        group_by = []
        for dim in dimensions:
            group_by.append(getattr(fact_model, dim))
        query = query.group_by(*group_by)

        return query

    @staticmethod
    def _add_joins(query, fact_model, dimensions):
        """Ajoute dynamiquement toutes les jointures nécessaires en fonction des dimensions demandées"""

        # Dictionnaire des relations possibles pour chaque modèle de fait
        relation_map = {
            'Visionnage': {
                'utilisateur': fact_model.utilisateur,
                'titre': fact_model.titre,
                'temps': fact_model.temps,
                'genre': fact_model.genre,
                'langue_disponible': fact_model.langue_disponible,
                'langue': fact_model.langue_disponible.property.mapper.class_,
                'abonnement': fact_model.utilisateur.property.mapper.abonnement
            },
            'Evaluation': {
                'utilisateur': fact_model.utilisateur,
                'titre': fact_model.titre,
                'temps': fact_model.temps,
                'genre': fact_model.genre
            },
            'Paiement': {
                'utilisateur': fact_model.utilisateur,
                'abonnement': fact_model.abonnement,
                'temps': fact_model.temps
            }
        }

        # Détection des relations nécessaires
        required_joins = set()
        for dim in dimensions:
            if '.' in dim:  # Relation imbriquée (ex: 'utilisateur.pays')
                relation = dim.split('.')[0]
                required_joins.add(relation)
            elif dim in relation_map[fact_model.__name__]:
                required_joins.add(dim)

        # Application des jointures
        joins_applied = set()
        for relation in required_joins:
            if relation in relation_map[fact_model.__name__] and relation not in joins_applied:
                relation_attr = relation_map[fact_model.__name__][relation]

                # Jointure standard
                query = query.join(relation_attr)

                # Jointures spéciales pour les relations indirectes
                if relation == 'langue':
                    query = query.join(fact_model.langue_disponible).join(relation_attr)
                elif relation == 'abonnement' and fact_model.__name__ == 'Visionnage':
                    query = query.join(fact_model.utilisateur).join(relation_attr)

                joins_applied.add(relation)

        return query