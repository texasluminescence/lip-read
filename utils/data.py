import glob
import os

import cv2
import torch
from torch.utils.data import Dataset

alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
blank_idx = 0
char2idx = {ch: i+1 for i, ch in enumerate(alphabet)} # Leave one blank token for CTC
idx2char = {v: k for k, v in char2idx.items()}

def text_to_int_sequence(text, char2idx):
    text = text.upper()
    sequence = []
    for ch in text:
        if ch in char2idx:
            sequence.append(char2idx[ch])
        # else be blank
    return sequence
    
class BBCNewsVideoDataset(Dataset):
    """
    A dataset that reads (video, transcript) pairs from 'pretrain' or 'main' directories.
    
    Each ID folder contains matching mp4/txt files named e.g. "00001.mp4" and "00001.txt".
    Parse the lines from .txt to extract the transcript text,
    and read frames from the corresponding .mp4 for the video data.
    """
    def __init__(self, 
                 root_dir,        # e.g. "/kaggle/input/my_data"
                 mode='pretrain', # or 'main'
                 transform=None,  # optional transforms on frames
                 max_frames=75):
        """
        :param root_dir: path to the folder containing 'pretrain' and 'main' subdirs
        :param mode: which subdir to read from ('pretrain' or 'main')
        :param transform: optional torchvision transforms for the frames
        :param max_frames: if you want to limit frames per clip (just an example)
        """
        super().__init__()
        self.root_dir = os.path.join(root_dir, mode)
        self.transform = transform
        self.max_frames = max_frames
        
        # Gather all mp4 files recursively
        # For example: root_dir/mode/*/*.mp4
        self.video_paths = sorted(glob.glob(os.path.join(self.root_dir, '*', '*.mp4')))
        
        # We'll derive the matching txt path by replacing .mp4 with .txt
        # or just see if it exists
        self.data = []
        for vp in self.video_paths:
            txt_path = vp.replace('.mp4', '.txt')
            if os.path.exists(txt_path):
                self.data.append((vp, txt_path))
            else:
                # If there's no matching txt, skip
                continue
                
    def __len__(self):
        return len(self.data)
    
    def parse_transcript(self, txt_path):
        """
        Reads the .txt file to extract the transcript text after 'Text:' line.
        For your example, we ignore Conf, WORD lines, etc.
        """
        transcript = ""
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("Text:"):
                    # Everything after "Text:" is the transcript
                    transcript = line.replace("Text:", "").strip()
                    # remove trailing "Conf:" if it's on the same line (some are multiline)
                    if "Conf:" in transcript:
                        transcript = transcript.split("Conf:")[0].strip()
                    break
        return transcript
    
    def read_video(self, video_path):
        """
        Reads frames from mp4 using OpenCV (cv2) into a list of frames (H,W,3).
        Optionally limit to self.max_frames frames.
        """
        frames = []
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            frame_count += 1
            if self.max_frames is not None and frame_count >= self.max_frames:
                break
        cap.release()
        return frames
    
    def __getitem__(self, idx):
        video_path, txt_path = self.data[idx]
        
        # Parse transcript
        transcript = self.parse_transcript(txt_path)
        
        # Read frames
        frames = self.read_video(video_path)  # list of np arrays, shape (H, W, 3)
        
        # Apply any transform to each frame
        if self.transform:
            frames = [self.transform(img) for img in frames]
        else:
            # Convert frames to torch Tensors if no transform
            # shape => (C, H, W)
            frames = [torch.from_numpy(img).permute(2,0,1) for img in frames]
        
        # Stack into a single tensor => shape (T, C, H, W)
        # T = number of frames
        video_tensor = torch.stack(frames, dim=0).float()

        # Return
        #   video_tensor: shape (T, 3, H, W)
        #   transcript: a string
        return video_tensor, transcript

# For padding the videos to have the same number of frames and converting the chars into nums for ctc
def collate_fn_ctc(batch):
    """
    batch: list of (frames, transcript_str)
        1) Convert transcript_str -> numeric
        2) Pad frames in time dimension
        3) Flatten targets
        4) Return (frames, targets, input_lengths, target_lengths)
    """
    # Sort by descending frames length
    batch.sort(key=lambda x: x[0].shape[0], reverse=True)

    frames_list, targets_list = [], []
    input_lengths, target_lengths = [], []
    max_len = 0

    for (video_tensor, txt) in batch:
        T = video_tensor.shape[0]
        if T > max_len:
            max_len = T
        
    # Convert text -> numeric, build up final batch
    for (video_tensor, txt) in batch:
        frames_list.append(video_tensor)
        input_lengths.append(video_tensor.shape[0])

        numeric_seq = text_to_int_sequence(txt, char2idx)
        target_lengths.append(len(numeric_seq))
        targets_list.append(torch.tensor(numeric_seq, dtype=torch.long))

    # Pad frames to max_len
    padded_frames = []
    for vid in frames_list:
        T = vid.shape[0]
        if T < max_len:
            pad_amt = max_len - T
            vid = torch.nn.functional.pad(vid, (0,0,0,0,0,0,0,pad_amt))  # pad time dim
        padded_frames.append(vid)
    
    frames_tensor = torch.stack(padded_frames, dim=0)  # => (B, max_len, C, H, W)
    concat_targets = torch.cat(targets_list, dim=0)
    
    input_lengths = torch.tensor(input_lengths, dtype=torch.long)
    target_lengths = torch.tensor(target_lengths, dtype=torch.long)
    
    return frames_tensor, concat_targets, input_lengths, target_lengths