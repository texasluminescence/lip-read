import time

import torch
from torch.nn import functional as F
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm

from utils.loss import Criterion
from utils.model import LipNet


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

    for batch in tqdm(train_dataloader, desc=f"Training (Epoch {epoch})", dynamic_ncols=True):
        frames, targets, input_lengths, target_lengths = batch

        # Send the inputs and targets to the training device
        frames = frames.to(device)
        targets = targets.to(device)

        frames = frames.permute(0, 2, 1, 3, 4)  # (B, T, C, H, W) => (B, C, T, H, W)
        
        logits = model(frames) # (batch_size, num_frames, num_classes)

        losses = criterion((logits, input_lengths), (targets, target_lengths))

        loss = losses["overall"]

        loss.backward()

        optimizer.step()
        optimizer.zero_grad()

def train(
        model: LipNet, 
        optimizer: Optimizer, 
        train_dataloader:  DataLoader, 
        criterion: Criterion, 
        num_epochs: int = 10, 
        device: torch.device = 'cuda'
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
    model.to(device)
    
    for epoch in range(num_epochs):
        train_one_epoch(model, optimizer, train_dataloader, criterion, epoch, device)
