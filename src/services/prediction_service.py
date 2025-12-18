from src.interfaces.prediction_interface import PredictionInterface
from src.predict import predict_image

class PredictionService(PredictionInterface):
    def predict(self, model_path, image_path):
        return predict_image(model_path, image_path)
