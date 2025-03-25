from flask import Request

def save_file(request: Request) -> None:
    file = request.files['file']
    file.save(f"utils/import.csv")