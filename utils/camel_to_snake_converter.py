import re
from typing import List

def list_camel_to_snake(liste: List[str]) -> List[str]:
    return [re.sub(r'(?<!^)(?=[A-Z])', '_', nom_attribut).lower() for nom_attribut in liste]

def str_camel_to_snake(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()