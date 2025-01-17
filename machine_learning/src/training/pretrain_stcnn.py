import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time
from tqdm import tqdm

from src.dataset.BBC_dataset import BBCNewsVideoDataset, collate_fn_ctc
from src.models.stcnn import PretrainSTCNN

def train_pretrain_stcnn(root_dir="data/mvlrs_v1",
                         epochs=5,
                         batch_size=256,
                         num_classes=28,
                         lr=1e-4,
                         device='cuda',
                         out_path="pretrain_stcnn.pth"):
    """
    Train the PretrainSTCNN model on 'pretrain' subset with a naive classification approach.
    Saves the model weights to out_path.
    """

    # 1) Create dataset/dataloader with mode='pretrain'
    transform = None  # or define a T.Compose if you want resizing
    dataset = BBCNewsVideoDataset(root_dir, mode='pretrain', transform=transform)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn_ctc)

    # 2) Build PretrainSTCNN
    model = PretrainSTCNN(num_classes=num_classes).to(device)

    # 3) Define optimizer & loss
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    print(f"Starting Pretraining on {len(dataset)} samples...")

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        start_time = time.time()

        for frames, transcripts, input_lengths, target_lengths in tqdm(loader, desc=f"Pretrain Epoch {epoch+1}"):
            # frames => shape (B, T, C, H, W)
            # transcripts => raw strings

            batch_size = frames.size(0)
            # TODO: create labels for this to train on
            label_tensor = torch.randint(0, num_classes, (batch_size,), device=device)

            # Reorder frames => (B, C, T, H, W)
            frames = frames.permute(0, 2, 1, 3, 4).to(device)

            optimizer.zero_grad()
            logits = model(frames)  # => (B, num_classes)
            loss = criterion(logits, label_tensor)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(loader)
        elapsed = time.time() - start_time
        print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Time: {elapsed:.2f}s")

    # 4) Save pretrained weights
    torch.save(model.state_dict(), out_path)
    print(f"Saved PretrainSTCNN model to {out_path}")
