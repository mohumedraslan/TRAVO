import os
import sys
import json
import torch

# Add the current directory to the path so we can import the train_model module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the training functions
from train_model import MonumentClassifier, train, save_model, MonumentDataset, device
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

def main():
    # Load monument names from labels.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    labels_path = os.path.join(current_dir, 'labels.json')
    
    with open(labels_path, 'r') as f:
        labels_data = json.load(f)
    
    monuments = labels_data.get('monuments', [])
    num_classes = len(monuments)
    
    print(f"Training model for {num_classes} monument classes...")
    
    # Create dataset
    dataset = MonumentDataset(os.path.join(current_dir, 'data'))
    
    # Split dataset into train and validation sets
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    # Create model
    model = MonumentClassifier(num_classes)
    
    # Train model
    print("Starting training...")
    model = train(model, train_loader, val_loader, num_epochs=5)
    
    # Save model
    model_path = os.path.join(current_dir, 'model.pth')
    save_model(model, model_path)
    
    print("Training completed successfully!")
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()