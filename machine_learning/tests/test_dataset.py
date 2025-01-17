from torch.utils.data import DataLoader
import torchvision.transforms as T

from src.dataset.BBC_dataset import BBCNewsVideoDataset, collate_fn_ctc

root_dir = "data/mvlrs_v1"

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((50,100)),  # (H, W)
    T.ToTensor()
])

# Create a dataset for the 'pretrain' directory
pretrain_dataset = BBCNewsVideoDataset(root_dir, mode='pretrain', transform=transform)
print("Pretrain dataset size:", len(pretrain_dataset))

# Example item
sample_video_tensor, sample_transcript = pretrain_dataset[0]
print("sample_video_tensor shape:", sample_video_tensor.shape)
print("sample_transcript:", sample_transcript)

# Create a DataLoader
pretrain_loader = DataLoader(pretrain_dataset, batch_size=2, shuffle=True, collate_fn=collate_fn_ctc)

# Example iteration
for batch in pretrain_loader:
    frames_tensor, concat_targets, input_lengths, target_lengths = batch
    print("Batch video frames:", len(frames_tensor))
    print("Batch transcript char length:", len(concat_targets))
    print("Batch frame nums:", input_lengths)
    print("Batch transcript lengths:", target_lengths)
    break