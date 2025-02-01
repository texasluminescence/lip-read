import argparse

from src.training.pretrain_stcnn import train_pretrain_stcnn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, default="data/mvlrs_v1", help="Path to dataset")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--num_classes", type=int, default=500, help="Classification head dimension")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--device", type=str, default="cuda", help="Device: cuda or cpu")
    parser.add_argument("--out_path", type=str, default="pretrain_stcnn.pth", help="Where to save model weights")

    args = parser.parse_args()

    train_pretrain_stcnn(
        root_dir=args.root_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        num_classes=args.num_classes,
        lr=args.lr,
        device=args.device,
        out_path=args.out_path
    )
    
# python scripts/run_pretrain.py --root_dir data/mvlrs_v1 --epochs 5 --batch_size 64 --num_classes 28
