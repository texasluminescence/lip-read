import argparse

class Config:
    CKPT_PATH = "checkpoints/ft_lrs3.pth"         # Update with your checkpoint path
    CNN_CKPT_PATH = "checkpoints/feature_extractor.pth"  # Update accordingly
    BUILDER = "vtp24x24"
    BEAM_SIZE = 30
    MAX_DECODE_LEN = 35
    DEVICE = "cuda"
    FEAT_DIM = 512
    NUM_BLOCKS = 6
    HIDDEN_UNITS = 512
    NUM_HEADS = 8
    DROPOUT_RATE = 0.1
    LM_ALPHA = 0.0
    IMG_SIZE = 96
    FRAME_SIZE = 160

def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt_path", default=Config.CKPT_PATH)
    parser.add_argument("--cnn_ckpt_path", default=Config.CNN_CKPT_PATH)
    parser.add_argument("--builder", default=Config.BUILDER)
    parser.add_argument("--beam_size", default=Config.BEAM_SIZE, type=int)
    parser.add_argument("--max_decode_len", default=Config.MAX_DECODE_LEN, type=int)
    parser.add_argument("--device", default=Config.DEVICE)
    parser.add_argument("--feat_dim", default=Config.FEAT_DIM, type=int)
    parser.add_argument("--num_blocks", default=Config.NUM_BLOCKS, type=int)
    parser.add_argument("--hidden_units", default=Config.HIDDEN_UNITS, type=int)
    parser.add_argument("--num_heads", default=Config.NUM_HEADS, type=int)
    parser.add_argument("--dropout_rate", default=Config.DROPOUT_RATE, type=float)
    parser.add_argument("--lm_alpha", default=Config.LM_ALPHA, type=float)
    parser.add_argument("--img_size", default=Config.IMG_SIZE, type=int)
    parser.add_argument("--frame_size", default=Config.FRAME_SIZE, type=int)
    return parser.parse_args([])
