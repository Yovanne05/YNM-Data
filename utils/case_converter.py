import re
from typing import List, Iterable


def list_camel_to_snake(liste: List[str]) -> List[str]:
    return [re.sub(r'(?<!^)(?=[A-Z])', '_', nom_attribut).lower() for nom_attribut in liste]

def str_camel_to_snake(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

def list_snake_to_camel(liste: Iterable[str]) -> List[str]:
    return [str_snake_to_camel(nom_attribut) for nom_attribut in liste]

def str_snake_to_camel(string: str) -> str:
    new_string = "".join(x.capitalize() for x in string.lower().split("_"))
    return string[0].lower() + new_string[1:]
