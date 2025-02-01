import torch.nn as nn
from .stcnn import STCNN

class LipNet(nn.Module):
    """
    Full lipreading model: STCNN + BiGRU + FC, trained with CTC.
    """
    def __init__(self, output_size=28, hidden_size=256, num_layers=2):
        super(LipNet, self).__init__()
        # Use STCNN as the feature extractor
        self.stcnn = STCNN()

        self.gru_hidden_size = hidden_size
        self.num_layers = num_layers

        # BiGRU
        self.gru = nn.GRU(
            input_size=self.stcnn.feature_dim,  # 1728
            hidden_size=self.gru_hidden_size,
            num_layers=self.num_layers,
            batch_first=True,
            bidirectional=True
        )

        # final linear layer
        self.fc = nn.Linear(hidden_size * 2, output_size)

    def forward(self, x):
        """
        x: shape (batch, 3, T, H, W)
        returns: (batch, T, output_size)
        """
        # 1) stcnn => (batch, T, feature_dim)
        feats = self.stcnn(x)  # => shape (B, T, 1728)

        # 2) BiGRU => shape (B, T, 2*hidden_size)
        out, _ = self.gru(feats)

        # 3) final projection
        logits = self.fc(out)  # => (B, T, output_size)
        return logits