from flask import Request

def save_file(request: Request) -> None:
    file = request.files['file']

    if file.mimetype not in ["text/csv", "application/vnd.ms-excel"]:
        raise Exception("Format de fichier non valide")

    file.save(f"utils/import.csv")