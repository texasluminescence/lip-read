import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as T
import os
import wandb
from dotenv import load_dotenv

from torch.utils.data import DataLoader

from src.utils.ctc_loss import Criterion
from src.dataset.BBC_dataset import BBCNewsVideoDataset, collate_fn_ctc
from src.models.lipnet import LipNet
from src.training.train_loop import train

if __name__ == "__main__":
    # Load .env file
    load_dotenv()

    # Define model and training parameters
    model = LipNet()

    if torch.cuda.device_count() > 1:
        print("Using DataParallel on", torch.cuda.device_count(), "GPUs!")
        model = torch.nn.DataParallel(model)
    
    model = model.cuda()
    ctc_loss = nn.CTCLoss(blank=0, reduction='mean', zero_infinity=True)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    # Generate DataLoader
    root_dir = "machine_learning/data/mvlrs_v1"
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize((50,100)),  # (H, W)
        T.ToTensor()
    ])
    
    # Set up dataloader
    criterion = Criterion()
    
    device = "cuda" if torch.cuda.is_available() else "cpu"

    main_dataset = BBCNewsVideoDataset(root_dir, mode='main', transform=transform)
    print("Main dataset size:", len(main_dataset))
    main_loader = DataLoader(main_dataset, batch_size=256, shuffle=True, collate_fn=collate_fn_ctc, num_workers=12)

    # Load Pretrained Parameters if available
    pretrained_dict = {}
    pretrained_path = "pretrain_stcnn.pth"

    if os.path.exists(pretrained_path):
        try:
            pretrained_dict = torch.load(pretrained_path)
            print(f"Loaded pretrained weights from {pretrained_path}")
        except Exception as e:
            print(f"Failed to load pretrained weights: {e}")
    else:
        print(f"No pretrained weights found at {pretrained_path}. Using random initialization.")

    model_dict = model.state_dict()
    filtered_dict = {}

    for k, v in pretrained_dict.items():
        # if it’s part of stcnn.* => copy
        if k.startswith("stcnn."):
            # rename if needed:
            new_key = k.replace("stcnn.", "stcnn.")
            if new_key in model_dict:
                filtered_dict[new_key] = v

    model.load_state_dict(filtered_dict, strict=False)

    # Init wandb
    wandb.init(project="LipRead", name="Test", tags=("Main"))
    
    # Train
    train(
        model=model,
        optimizer=optimizer,
        train_dataloader=main_loader,
        criterion=criterion,
        num_epochs=100,
        device=device
    )
    
# python scripts/run_train.py