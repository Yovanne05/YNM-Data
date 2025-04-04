class ModelRegistry:
    def __init__(self):
        self._models = {}

    def register(self, name, model):
        self._models[name] = model
        setattr(self, name, model)

    def __getitem__(self, key):
        """Permet l'accès via db.models['NomModele']"""
        return self._models[key]

    def get(self, key, default=None):
        return self._models.get(key, default)