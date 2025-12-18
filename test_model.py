import torch
from torchvision import models, transforms
from PIL import Image
import os
from torch import nn

# ===============================
# LOAD MODEL
# ===============================
model_path = "models/rice_model.pth"   # or pulse_model.pth

print("\nLoading trained model...\n")

checkpoint = torch.load(model_path, map_location="cpu")

# Extract saved data
state_dict = checkpoint["model_state"]
class_names = checkpoint["classes"]

# Rebuild model
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(state_dict)
model.eval()

print("Model loaded successfully")
print("Classes:", class_names)

# ===============================
# IMAGE TRANSFORMS
# ===============================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ===============================
# TEST MULTIPLE IMAGES
# ===============================
test_folder = "data/ricedataset"  # change to Bean_Dataset if needed

print("\nTesting multiple images...\n")

for root, dirs, files in os.walk(test_folder):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(root, file)

            try:
                img = Image.open(img_path).convert("RGB")
                img_t = transform(img).unsqueeze(0)

                with torch.no_grad():
                    outputs = model(img_t)
                    probs = torch.softmax(outputs, dim=1)
                    conf, predicted = torch.max(probs, 1)

                print(f"Image: {file}")
                print(
                    f"Prediction: {class_names[predicted.item()]} "
                    f"({conf.item() * 100:.2f}%)"
                )
                print("-" * 60)

            except Exception as e:
                print(f"Error reading image {file}: {str(e)}")
