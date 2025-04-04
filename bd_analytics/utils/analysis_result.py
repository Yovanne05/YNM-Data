from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AnalysisResult:
    """Classe pour standardiser les résultats d'analyse"""
    data: List[Dict]
    meta: Dict
