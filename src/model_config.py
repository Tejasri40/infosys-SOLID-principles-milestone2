# src/model_config.py

# This module acts as a configuration layer for models
# Helps apply Dependency Inversion & Open–Closed Principles

MODELS = {
    "Rice": "models/rice_model.pth",
    "Pulse": "models/pulse_model.pth"
}

def get_model_path(model_name: str) -> str:
    """
    Returns the model path for the selected crop.
    This keeps model details outside the UI layer.
    """
    return MODELS[model_name]
