from src.utils.ctc_decode import greedy_decode_ctc

def levenshtein_distance(ref, hyp):
    """
    Compute the Levenshtein distance (edit distance) between two sequences.
    ref: list of int (ground truth)
    hyp: list of int (predicted)
    """
    # We'll build a 2D DP array where dp[i][j] represents the edit distance
    # between ref[:i] and hyp[:j].
    
    # lengths
    m, n = len(ref), len(hyp)
    
    # Create a matrix (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # If one sequence is empty, distance = length of the other
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill in the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # same char => no additional edit
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # deletion
                    dp[i][j - 1],    # insertion
                    dp[i - 1][j - 1] # substitution
                )
    return dp[m][n]

def compute_accuracy(logits, targets, input_lengths, target_lengths, blank=0):
    """
    Computes accuracy = 1 - (Character Error Rate),
    where CER is (LevenshteinDistance / reference_length).
    
    logits: (B, T, vocab_size)
    targets: 1D Tensor of size (total_target_tokens_in_batch,)
    input_lengths: length of each sequence in frames (list/tensor, shape [B])
    target_lengths: length of each transcript (list/tensor, shape [B])
    blank: index for blank symbol (default=0)
    """
    batch_size = len(input_lengths)
    
    # 1) Greedy decode
    decoded_preds = greedy_decode_ctc(logits, blank=blank)  # list of lists
    
    # 2) Reconstruct each target sequence from the 1D 'targets'
    target_splits = []
    idx = 0
    for length in target_lengths:
        seq = targets[idx:idx + length].tolist()
        target_splits.append(seq)
        idx += length
    
    # We'll accumulate total distance and total chars
    total_distance = 0
    total_chars = 0
    
    # 3) For each pair, compute the Levenshtein distance
    for i in range(batch_size):
        ref_seq = target_splits[i]
        hyp_seq = decoded_preds[i]
        
        distance = levenshtein_distance(ref_seq, hyp_seq)
        total_distance += distance
        total_chars += len(ref_seq)  # normalizing by length of reference
    
    # Avoid divide by zero
    if total_chars == 0:
        return 1.0  # if there's literally no ground-truth chars, treat as 100% (or do something else)
    
    # CER (Character Error Rate) = total_distance / total_chars
    cer = total_distance / total_chars
    accuracy = 1.0 - cer
    
    return accuracy
