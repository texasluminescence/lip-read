import torch
import wandb
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm
import os

from src.utils.ctc_loss import Criterion
from src.models.lipnet import LipNet


def train_one_epoch(
        model: LipNet,
        optimizer: Optimizer,
        train_dataloader: DataLoader,
        criterion: Criterion,
        epoch: int,
        device: torch.device = 'cuda'
    ) -> None:
    """
    Args:
        model: LipNet model
        optimizer: Optimizer
        train_dataloader: DataLoader yielding (frames, targets, input_lengths, target_lengths)
        Criterion: Loss function
        device: Device to train on
    """

    model.train()
    total_loss = 0.0
    num_samples = 0

    for batch in tqdm(train_dataloader, desc=f"Training (Epoch {epoch})", dynamic_ncols=True):
        frames, targets, input_lengths, target_lengths = batch

        # Send the inputs and targets to the training device
        frames = frames.to(device)
        targets = targets.to(device)

        # (batch_size, num_frames, num_channels, height, width) => (batch_size, num_channels, num_frames, height, width)
        frames = frames.permute(0, 2, 1, 3, 4)
        
        # (batch_size, num_frames, num_classes)
        logits = model(frames)

        losses = criterion((logits, input_lengths), (targets, target_lengths))

        wandb.log({"Train": {"Loss": losses}}, step=wandb.run.step + len(frames))

        loss = losses["overall"]

        loss.backward()

        optimizer.step()
        optimizer.zero_grad()
        
        # For average loss
        batch_size = frames.size(0)
        total_loss += loss.item() * batch_size
        num_samples += batch_size
        
    avg_loss = total_loss / num_samples if num_samples > 0 else 0.0
    return avg_loss

def train(
        model: LipNet, 
        optimizer: Optimizer, 
        train_dataloader:  DataLoader, 
        criterion: Criterion, 
        num_epochs: int = 10, 
        device: torch.device = 'cuda',
        checkpoint_dir: str = "checkpoints"
    ) -> None:
    """
    Args:
        model: LipNet model
        optimizer: Optimizer
        train_dataloader: DataLoader yielding (frames, targets, input_lengths, target_lengths)
        Criterion: Loss function
        num_epochs: Number of epochs to train for
        device: Device to train on
    """
    os.makedirs(checkpoint_dir, exist_ok=True)
    model.to(device)
    
    for epoch in range(num_epochs):
        avg_loss = train_one_epoch(model, optimizer, train_dataloader, criterion, epoch, device)

        print(f"Epoch [{epoch+1}/{num_epochs}] - Avg Train Loss: {avg_loss:.4f}")

        # Save model checkpoint after each epoch
        checkpoint_path = os.path.join(checkpoint_dir, f"machine_learning/lipnet_epoch_{epoch+1}.pth")
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": avg_loss
        }, checkpoint_path)
        print(f"Model checkpoint saved to {checkpoint_path}")
