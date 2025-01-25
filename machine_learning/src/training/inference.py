import torch
from src.utils.ctc_decode import greedy_decode_ctc

def run_inference_single(model, frames, idx2char=None, blank_idx=0, device='cuda'):
    """
    Args:
      model: your LipNet model (or DataParallel version).
      frames: shape (T, C, H, W) for 1 sample 
              OR (B, T, C, H, W) for multiple samples.
      idx2char: dict mapping token_id -> character
      blank_idx: integer for the blank token
      device: 'cuda' or 'cpu'

    Returns:
      A list of predicted sequences (list of IDs or strings).
    """
    model.eval()

    # If frames is just (T,C,H,W), add batch dimension => (1,T,C,H,W)
    if frames.dim() == 4:
        frames = frames.unsqueeze(0)

    # Reorder to (B, C, T, H, W)
    # Currently we have (B, T, C, H, W), so do frames.permute(0,2,1,3,4)
    frames = frames.to(device)
    frames = frames.permute(0, 2, 1, 3, 4)

    with torch.no_grad():
        logits = model(frames)  # => (B, T, vocab_size)

    # Greedy decode
    decoded_ids_batch = greedy_decode_ctc(logits, blank=blank_idx)

    # Convert IDs to strings
    decoded_strs = []
    if idx2char is not None:
        for seq_ids in decoded_ids_batch:
            s = "".join(idx2char[i] for i in seq_ids)
            decoded_strs.append(s)
        return decoded_strs
    else:
        return decoded_ids_batch