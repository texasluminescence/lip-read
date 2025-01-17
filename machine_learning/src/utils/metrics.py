import torch
from utils.ctc_decode import greedy_decode_ctc

def compute_accuracy(model, frames, targets, input_lengths, target_lengths, blank_idx=0, device='cuda'):
    """
    Measures "exact match" accuracy for a batch. 
    frames => (B, T, C, H, W)
    targets => 1D cat of all target IDs for CTC
    input_lengths => length of each video in frames
    target_lengths => length of each transcript

    This code:
      1) forward pass
      2) greedy decode
      3) reconstruct each ground-truth sequence from 'targets'
      4) compare if predicted = ground-truth EXACTly

    Return: float in [0,1]
    """
    model.eval()
    with torch.no_grad():
        # re-permute frames => (B, C, T, H, W)
        frames = frames.permute(0, 2, 1, 3, 4).to(device)
        logits = model(frames)  # => (B, T, vocab_size)
        # Greedy decode
        preds = greedy_decode_ctc(logits, blank=blank_idx)  # list of lists of token IDs

    # Now we split 'targets' by target_lengths to get each sample's ground truth
    gt_splits = []
    idx = 0
    for length in target_lengths:
        seq = targets[idx:idx+length].tolist()
        gt_splits.append(seq)
        idx += length

    # Compare
    batch_size = frames.size(0)
    correct = 0
    for i in range(batch_size):
        if preds[i] == gt_splits[i]:
            correct += 1

    return correct / batch_size
