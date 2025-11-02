import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import cv2
import json
from typing import Tuple, List, Dict, Any

# Set random seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Define paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pth')
LABELS_PATH = os.path.join(os.path.dirname(__file__), 'labels.json')

# Check if CUDA is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define a simple CNN model for monument classification
class MonumentClassifier(nn.Module):
    def __init__(self, num_classes: int):
        super(MonumentClassifier, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(128 * 28 * 28, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# Custom dataset class for monument images
class MonumentDataset(Dataset):
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load labels
        with open(LABELS_PATH, 'r') as f:
            label_data = json.load(f)
            self.label_map = {monument['name']: idx for idx, monument in enumerate(label_data.get('monuments', []))}
        
        # In a real implementation, this would load actual image data
        # For this example, we'll generate synthetic data
        for label_name, label_idx in self.label_map.items():
            for i in range(10):  # 10 synthetic images per monument
                img_path = f"{label_name}_{i}.jpg"
                self.images.append(img_path)
                self.labels.append(label_idx)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # In a real implementation, this would load the actual image
        # For this example, we'll generate a random image
        img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        
        if self.transform:
            img = self.transform(img)
        
        # Convert to tensor
        img = torch.from_numpy(img.transpose((2, 0, 1))).float() / 255.0
        
        return img, label

def train(model, train_loader, val_loader, num_epochs=10):
    # Define loss function and optimizer
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Move model to device
    model.to(device)
    
    # Training loop
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for inputs, labels in train_loader:
            # Move data to device
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Statistics
            train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        train_loss = train_loss / len(train_loader.dataset)
        train_acc = train_correct / train_total
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        # No gradient calculation during validation
        with torch.no_grad():
            for inputs, labels in val_loader:
                # Move data to device
                inputs, labels = inputs.to(device), labels.to(device)
                
                # Forward pass
                outputs = model(inputs)
                loss = loss_fn(outputs, labels)
                
                # Statistics
                val_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_correct / val_total
        
        print(f'Epoch {epoch+1}/{num_epochs}, '
              f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, '
              f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}')
    
    return model

def save_model(model, path):
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")

def load_model(num_classes, path):
    model = MonumentClassifier(num_classes)
    model.load_state_dict(torch.load(path))
    model.to(device)
    model.eval()
    return model

if __name__ == "__main__":
    # Create dataset and dataloaders
    dataset = MonumentDataset(DATA_DIR)
    
    # Split dataset into train and validation sets
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    # Create model
    num_classes = len(dataset.label_map)
    model = MonumentClassifier(num_classes)
    
    # Train model
    model = train(model, train_loader, val_loader)
    
    # Save model
    save_model(model, MODEL_PATH)
    
    print("Training completed successfully!")