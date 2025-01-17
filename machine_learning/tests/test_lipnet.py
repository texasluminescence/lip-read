import torch
from src.models.lipnet import LipNet

# quick test with a dummy input:
if __name__ == "__main__":
    model = LipNet()
    # dummy input: batch=2, channels=3, frames=75, H=50, W=100
    dummy_input = torch.randn(2, 3, 75, 50, 100)
    out = model(dummy_input)
    print("Output shape:", out.shape)
    # Should be (2, 75, 28)