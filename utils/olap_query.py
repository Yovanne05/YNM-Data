from operator import and_


def build_aggregation_query(session, fact_model, dimensions, measures, filters=None):
    """
    Construit une requête d'agrégation OLAP
    """
    from sqlalchemy import func

    # Colonnes à sélectionner
    select_columns = []

    # Traitement des dimensions
    for dim in dimensions:
        if hasattr(fact_model, dim):
            select_columns.append(getattr(fact_model, dim))
        else:
            # Gestion des relations
            rel, field = dim.split('.')
            related_model = getattr(fact_model, rel).property.mapper.class_
            select_columns.append(getattr(related_model, field))

    # Traitement des mesures
    agg_functions = {
        'count': func.count,
        'sum': func.sum,
        'avg': func.avg,
        'min': func.min,
        'max': func.max
    }

    for measure in measures:
        if '(' in measure:  # Mesure avec fonction d'agrégation
            agg_func, col = measure.split('(')
            col = col.rstrip(')')
            if agg_func in agg_functions:
                select_columns.append(agg_functions[agg_func](getattr(fact_model, col)).label(measure))
        else:
            select_columns.append(getattr(fact_model, measure))

    # Construction de la requête de base
    query = session.query(*select_columns)

    # Ajout des jointures pour les relations
    for dim in dimensions:
        if '.' in dim:
            rel = dim.split('.')[0]
            query = query.join(getattr(fact_model, rel))

    # Application des filtres
    if filters:
        filter_conditions = []
        for key, value in filters.items():
            if '.' in key:  # Filtre sur relation
                rel, field = key.split('.')
                related_model = getattr(fact_model, rel).property.mapper.class_
                filter_conditions.append(getattr(related_model, field) == value)
            else:
                filter_conditions.append(getattr(fact_model, key) == value)
        query = query.filter(and_(*filter_conditions))

    # Group by
    group_by_cols = []
    for dim in dimensions:
        if hasattr(fact_model, dim):
            group_by_cols.append(getattr(fact_model, dim))
        else:
            rel, field = dim.split('.')
            related_model = getattr(fact_model, rel).property.mapper.class_
            group_by_cols.append(getattr(related_model, field))

    return query.group_by(*group_by_cols)