import torch.nn.functional as F
from tqdm import tqdm
import time

def train_step(frames, targets, input_lengths, target_lengths, model, optimizer, ctc_loss):
    frames = frames.cuda()
    targets = targets.cuda()

    optimizer.zero_grad()
    
    logits = model(frames)  # (batch, time, output_size)
    # For CTC => (T, N, C)
    logits_for_ctc = logits.permute(1, 0, 2)
    
    log_probs = F.log_softmax(logits_for_ctc, dim=2)
    loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)
    loss.backward()
    optimizer.step()
    return loss.item()

def train_model(model, train_loader, ctc_loss, optimizer, num_epochs=10, device='cuda'):
    """
    Args:
        model: your LipNetPyTorch model
        train_loader: DataLoader yielding (frames, targets, input_lengths, target_lengths)
        ctc_loss: nn.CTCLoss (or similar)
        optimizer: e.g. torch.optim.Adam(model.parameters())
        num_epochs: total epochs to train
        device: 'cuda' or 'cpu'
    """
    
    model.to(device)
    model.train()
    
    for epoch in range(num_epochs):
        epoch_start = time.time()
        total_loss = 0.0
        
        for batch_idx, (frames, targets, input_lengths, target_lengths) in enumerate(
            tqdm(train_loader, desc=f"Epoch {epoch+1}", unit="batch")
        ):
            # frames => (B, T, C, H, W), need (B, C, T, H, W)
            frames = frames.permute(0, 2, 1, 3, 4)
            loss_value = train_step(frames, targets, input_lengths, target_lengths, model, optimizer, ctc_loss)
            total_loss += loss_value
        
        avg_loss = total_loss / len(train_loader)
        epoch_time = time.time() - epoch_start
        print(f"Epoch [{epoch+1}/{num_epochs}] took {epoch_time:.2f} seconds, Loss: {avg_loss:.4f}")