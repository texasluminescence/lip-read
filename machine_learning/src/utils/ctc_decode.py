def greedy_decode_ctc(logits, blank=0):
    """
    Greedy decodes the model's output for a batch of samples.
    logits shape: (batch, time, vocab_size)
      (e.g., from LipNet forward pass).
    Returns: a list of lists, where each sub-list is the decoded token IDs for that sample.
    """
    # Argmax over the vocab dimension => shape (batch, time)
    argmax_ids = logits.argmax(dim=2)

    decoded_sequences = []
    for b in range(argmax_ids.size(0)):
        seq_ids = argmax_ids[b].tolist()

        filtered = []
        prev = None
        for token_id in seq_ids:
            if token_id != blank and token_id != prev:
                filtered.append(token_id)
            prev = token_id
        decoded_sequences.append(filtered)
    return decoded_sequences
