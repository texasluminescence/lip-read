from torch import nn
from torch.nn import functional as F


class LipNet(nn.Module):
    def __init__(self,
                 img_c=3,
                 img_w=100,
                 img_h=50,
                 frames_n=75,
                 output_size=28,        # number of characters + 1 for blank
                 absolute_max_string_len=32  # not strictly needed in PyTorch model??
                 ):
        super(LipNet, self).__init__()
        
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
        
        # After these 3D convs, the shape in time dimension should remain ~frames_n
        # but height/width get downsampled heavily by stride/pool
        # We'll flatten spatial dims but keep the time dim for the RNN

        # Dimensionality going into the GRUs:
        # original: (W=100, H=50)
        # conv1+pool1 => W -> (100/2/2)=25, H->(50/2/2)=12 (accounting for strides/pools)
        # conv2+pool2 => W -> 25/2=12,   H->12/2=6
        # conv3+pool3 => W -> 12/2=6,    H->6/2=3
        # => final is (N, 96, T, 3, 6)
        # => flattened per frame => 96*3*6 = 1728

        self.gru_hidden_size = 256
        self.num_gru_layers = 2
        
        # Bi-directional GRU
        self.gru = nn.GRU(input_size=1728,
                          hidden_size=self.gru_hidden_size,
                          num_layers=self.num_gru_layers,
                          batch_first=True,
                          bidirectional=True)
        
        # Final linear layer to project onto output_size
        # Because it’s bidirectional, output size is 2 * gru_hidden_size
        self.fc = nn.Linear(self.gru_hidden_size * 2, output_size)

    def forward(self, x):
        """
        x shape expected as (batch, channels=3, frames=75, height=50, width=100)
        If your data is (batch, frames, height, width, channels),
        be sure to permute it before calling forward: x.permute(0,4,1,2,3)
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
        # x shape is (batch, 96, T, H’, W’)
        b, c, t, h, w = x.size()
        # -> (batch, t, c*h*w)
        x = x.permute(0, 2, 1, 3, 4)
        x = x.reshape(b, t, c*h*w)
        
        # (4) Bi-GRU
        # x => shape (batch, time, features)
        x, _ = self.gru(x)  # => (batch, time, 2*gru_hidden_size)

        # (5) FC => output_size
        logits = self.fc(x)  # => (batch, time, output_size)

        # For CTC, you’ll typically feed log_probs = F.log_softmax(logits, dim=2)
        return logits