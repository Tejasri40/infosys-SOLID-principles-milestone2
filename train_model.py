import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

# ==========================
# CONFIG
# ==========================
DATA_DIR = "data/ricedataset"
MODEL_SAVE_PATH = "models/rice_model.pth"


EPOCHS = 20
BATCH_SIZE = 16
LR = 0.001


def train_model():
    print("\n" + "=" * 45)
    print("LOADING DATASET")
    print("=" * 45)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    dataset = datasets.ImageFolder(DATA_DIR, transform=transform)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_data, val_data = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )

    print(f"Training samples: {len(train_data)}")
    print(f"Validation samples: {len(val_data)}\n")

    print(f"Model will train for {len(dataset.classes)} classes: {dataset.classes}\n")

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE)

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    best_val_acc = 0.0
    best_state = None

    print("=" * 45)
    print("STARTING TRAINING")
    print("=" * 45)

    for epoch in range(EPOCHS):
        # ---------------- TRAIN ----------------
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_acc = 100 * correct / total

        # ---------------- VALIDATION ----------------
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, preds = torch.max(outputs, 1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        val_acc = 100 * correct / total

        # ---------------- LOG ----------------
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")

        # ---------------- SAVE BEST MODEL ----------------
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = model.state_dict()

            checkpoint = {
                "model_state": best_state,
                "classes": dataset.classes
            }

            torch.save(checkpoint, MODEL_SAVE_PATH)
            print(f"✓ Best model saved! (Epoch {epoch+1}, Acc: {val_acc:.2f}%)")


if __name__ == "__main__":
    train_model()
