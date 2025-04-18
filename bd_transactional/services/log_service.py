from typing import List, Tuple
import datetime

logs: List[Tuple[str, str]] = []

def add_logs(msg: str):
    timestamp = datetime.datetime.now().isoformat()
    logs.append((timestamp, msg))

def get_logs() -> List[Tuple[str, str]]:
    return logs

def clear_logs():
    logs.clear()