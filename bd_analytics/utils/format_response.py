from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd


def format_response(
        success: bool,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format standard de réponse API

    Args:
        success: Indique si la requête a réussi (booléen)
        data: Données principales de la réponse (dict, list ou DataFrame)
        error: Message d'erreur en cas d'échec
        metadata: Métadonnées supplémentaires sur la réponse

    Returns:
        Dictionnaire de réponse standardisé
    """
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }

    if data is not None:
        if isinstance(data, pd.DataFrame):
            response['data'] = data.to_dict(orient='records')
        else:
            response['data'] = data

    if error:
        response['error'] = error

    if metadata:
        response['metadata'] = metadata

    return response
