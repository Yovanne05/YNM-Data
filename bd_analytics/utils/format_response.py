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
    Standard API response format

    Args:
        success: Whether the request was successful
        data: Main response data (dict, list, or DataFrame)
        error: Error message if not successful
        metadata: Additional metadata about the response

    Returns:
        Standardized response dictionary
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