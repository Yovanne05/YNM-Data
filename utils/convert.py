import re

def snake_to_camel(text: str) -> str:
    """
    Convertit un texte en snake_case en camelCase.
    Exemple : 'id_langue_disponible' -> 'idLangueDisponible'
    """
    components = text.lower().split('_')  # Assure-toi que tout est en minuscule
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(name: str) -> str:
    """
    Convertit un texte en camelCase en snake_case.
    Exemple : 'idLangueDisponible' -> 'id_langue_disponible'
    """
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()
