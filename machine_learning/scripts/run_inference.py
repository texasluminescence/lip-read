import argparse
import torch
import torchvision.transforms as T
import cv2

from src.training.inference import run_inference_single
from src.utils.tokenizer import int_to_text_sequence
from src.models.lipnet import LipNet

def load_video_frames(path, max_frames=75):
    frames = []
    cap = cv2.VideoCapture(path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
        count += 1
        if count >= max_frames:
            break
    cap.release()
    return frames

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--model_ckpt", type=str, default="checkpoints/lipnet_epoch_1.pth")
    args = parser.parse_args()

    # Load model
    model = LipNet()
    model.load_state_dict(torch.load(args.model_ckpt, weights_only=True)["model_state_dict"])
    model.cuda()

    # Prep frames
    raw_frames = load_video_frames(args.video_path, max_frames=75)
    # apply transform:
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize((50,100)),
        T.ToTensor()
    ])
    frames_tensor = [transform(f) for f in raw_frames]
    frames_tensor = torch.stack(frames_tensor, dim=0)  # => (T, C, H, W)

    # Run inference
    pred = run_inference_single(model, frames_tensor, idx2char=None, blank_idx=0, device='cuda')
    print("Prediction:", int_to_text_sequence(pred[0]))


# python machine_learning/scripts/run_inference.py --video_path machine_learning/data/mvlrs_v1/main/5535415699068794046/00001.mp4 --model_ckpt machine_learning/checkpoints/lipnet_epoch_100.pth
