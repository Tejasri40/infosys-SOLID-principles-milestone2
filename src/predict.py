import torch
from torchvision import transforms, models
from PIL import Image
import streamlit as st

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


@st.cache_resource
def load_model(model_path):
    checkpoint = torch.load(model_path, map_location=DEVICE)

    if not isinstance(checkpoint, dict):
        raise ValueError("Invalid checkpoint format")

    if "model_state" not in checkpoint or "classes" not in checkpoint:
        raise ValueError("Checkpoint must contain 'model_state' and 'classes'")

    state_dict = checkpoint["model_state"]
    class_names = checkpoint["classes"]

    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))

    model.load_state_dict(state_dict)
    model.to(DEVICE)
    model.eval()

    return model, class_names


def preprocess_image(img_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    img = Image.open(img_path).convert("RGB")
    img = transform(img).unsqueeze(0)
    return img.to(DEVICE)


def predict_image(model_path, img_path):
    model, class_names = load_model(model_path)
    img = preprocess_image(img_path)

    with torch.no_grad():
        output = model(img)
        probs = torch.softmax(output, dim=1)
        confidence, pred = torch.max(probs, 1)

    return class_names[pred.item()], confidence.item() * 100
