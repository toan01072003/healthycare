class DummyModel:
    def __init__(self):
        self.classes_ = ['disease_a', 'disease_b']
    def predict_proba(self, X):
        return [[0.6, 0.4] for _ in range(len(X))]

class DummyEncoder:
    def __init__(self):
        self.classes_ = ['symptom_a', 'symptom_b']
    def transform(self, X):
        return X
