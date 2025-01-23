import torch.nn as nn
import torch.nn.functional as F

class STCNN(nn.Module):
    """
    Spatiotemporal CNN backbone that produces a (batch, time, feature_dim) output,
    which can be fed into a sequence model (like Bi-GRU).
    """
    def __init__(self,
                 img_c=3,
                 img_w=100,
                 img_h=50,
                 frames_n=75,
                 ):
        super(STCNN, self).__init__()

        # 3D Conv block #1
        self.conv1 = nn.Conv3d(in_channels=img_c,
                               out_channels=32,
                               kernel_size=(3, 5, 5),
                               stride=(1, 2, 2),
                               padding=(1, 2, 2))
        self.pool1 = nn.MaxPool3d(kernel_size=(1, 2, 2),
                                  stride=(1, 2, 2))
        self.drop1 = nn.Dropout(0.5)

        # 3D Conv block #2
        self.conv2 = nn.Conv3d(in_channels=32,
                               out_channels=64,
                               kernel_size=(3, 5, 5),
                               stride=(1, 1, 1),
                               padding=(1, 2, 2))
        self.pool2 = nn.MaxPool3d(kernel_size=(1, 2, 2),
                                  stride=(1, 2, 2))
        self.drop2 = nn.Dropout(0.5)

        # 3D Conv block #3
        self.conv3 = nn.Conv3d(in_channels=64,
                               out_channels=96,
                               kernel_size=(3, 3, 3),
                               stride=(1, 1, 1),
                               padding=(1, 1, 1))
        self.pool3 = nn.MaxPool3d(kernel_size=(1, 2, 2),
                                  stride=(1, 2, 2))
        self.drop3 = nn.Dropout(0.5)

        # Dimensionality going into the GRUs:
        # original: (W=100, H=50)
        # conv1+pool1 => W -> (100/2/2)=25, H->(50/2/2)=12 (accounting for strides/pools)
        # conv2+pool2 => W -> 25/2=12,   H->12/2=6
        # conv3+pool3 => W -> 12/2=6,    H->6/2=3
        # => final is (N, 96, T, 3, 6)
        # => flattened per frame => 96*3*6 = 1728
        self.feature_dim = 96*3*6 

    def forward(self, x):
        """
        x shape: (batch, channels=3, frames=75, height=50, width=100)
        returns shape: (batch, T, self.feature_dim)
        """
        # (1) 3D conv/pool #1
        x = self.conv1(x)  # => (batch, 32, frames, H/2, W/2)
        x = F.relu(x)
        x = self.pool1(x)  # => (batch, 32, frames, H/4, W/4)
        x = self.drop1(x)
        
        # (2) 3D conv/pool #2
        x = self.conv2(x)  # => (batch, 64, frames, H/4, W/4)
        x = F.relu(x)
        x = self.pool2(x)  # => (batch, 64, frames, H/8, W/8)
        x = self.drop2(x)
        
        # (3) 3D conv/pool #3
        x = self.conv3(x)  # => (batch, 96, frames, H/8, W/8)
        x = F.relu(x)
        x = self.pool3(x)  # => (batch, 96, frames, H/16, W/16)
        x = self.drop3(x)

        # Now flatten the spatial dims but keep the time dim
        # x shape => (batch, 96, T, 3, 6)
        b, c, t, h, w = x.shape
        # reorder => (batch, T, c, h, w)
        x = x.permute(0, 2, 1, 3, 4).contiguous()
        # flatten => (batch, T, 96*3*6)
        x = x.view(b, t, self.feature_dim)

        return x


class PretrainSTCNN(nn.Module):
    """
    A small classification model that reuses STCNN as a feature extractor,
    then adds a simple classification head (e.g., for word-level pretraining).
    """
    def __init__(self, num_classes=500):
        super(PretrainSTCNN, self).__init__()
        self.stcnn = STCNN()
        # Average pooling over T and then a FC:
        self.classifier = nn.Linear(self.stcnn.feature_dim, num_classes)

    def forward(self, x):
        """
        x: shape (batch, 3, T, H, W)
        returns logits: (batch, num_classes)
        """
        # Extract spatiotemporal features => (batch, T, feature_dim)
        feats = self.stcnn(x)
        # feats shape => (batch, T, feature_dim)

        # Just average pool over T
        feats_avg = feats.mean(dim=1)  # => (batch, feature_dim)

        # final classification
        logits = self.classifier(feats_avg)  # => (batch, num_classes)
        return logits