from abc import ABC, abstractmethod

class PredictionInterface(ABC):
    @abstractmethod
    def predict(self, model_path, image_path):
        pass
