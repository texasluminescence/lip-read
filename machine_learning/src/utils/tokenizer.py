ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
char2idx = {character: i + 1 for i, character in enumerate(ALPHABET)} # Leave one blank token for CTC

def text_to_int_sequence(text):
    text = text.upper()
    sequence = []
    for char in text:
        if char in char2idx:
            sequence.append(char2idx[char])
        # else be blank
    return sequence

def int_to_text_sequence(sequence):
    text = ""
    for i in sequence:
        text += ALPHABET[i-1]
    return text