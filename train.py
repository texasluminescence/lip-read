import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms as T

import wandb
from utils.data import BBCNewsVideoDataset, collate_fn_ctc
from machine_learning.src.utils.ctc_loss import Criterion
from utils.model import LipNet
from machine_learning.src.training.train_loop import train

device = "cuda" if torch.cuda.is_available() else "cpu"

# Create the model, optimizer, and loss function
model = LipNet()

optimizer = optim.Adam(model.parameters(), lr=1e-4)

criterion = Criterion()

# Create the dataset
root_dir = "data/mvlrs_v1"

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((50,100)),  # (H, W) 
    T.ToTensor()
])

train_dataset = BBCNewsVideoDataset(root_dir, mode='main', transform=transform)

train_dataloader = DataLoader(
    train_dataset,
    batch_size=192,
    shuffle=True, 
    collate_fn=collate_fn_ctc,
    num_workers=12
)

wandb.init(project="LipRead", name="Test", tags=("Main"))

train(
    model=model,
    optimizer=optimizer,
    train_dataloader=train_dataloader,
    criterion=criterion,
    num_epochs=10,
    device=device
)