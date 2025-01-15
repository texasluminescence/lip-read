import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms as T

from utils.data import BBCNewsVideoDataset, collate_fn_ctc
from utils.model import LipNetPyTorch
from utils.processor import train_model

model = LipNetPyTorch()
if torch.cuda.device_count() > 1:
    print("Using DataParallel on", torch.cuda.device_count(), "GPUs!")
    model = torch.nn.DataParallel(model)
model = model.cuda()
ctc_loss = nn.CTCLoss(blank=0, reduction='mean', zero_infinity=True)
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Set up dataloader
root_dir = "data/mvlrs_v1"

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((50,100)),  # (H, W) 
    T.ToTensor()
])

main_dataset = BBCNewsVideoDataset(root_dir, mode='main', transform=transform)
print("Main dataset size:", len(main_dataset))
main_loader = DataLoader(main_dataset, batch_size=32, shuffle=True, collate_fn=collate_fn_ctc)

train_model(model, main_loader, ctc_loss, optimizer, num_epochs=1, device='cuda')