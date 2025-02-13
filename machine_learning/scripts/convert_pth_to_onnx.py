import torch
import argparse
from src.models.lipnet import LipNet

def main():
    parser = argparse.ArgumentParser(description="Export LipNet model to ONNX format.")
    parser.add_argument("--checkpoint", type=str, required=True,
                        help="Path to the LipNet .pth checkpoint file.")
    parser.add_argument("--output", type=str, default="lipnet.onnx",
                        help="Path to save the exported ONNX model.")
    args = parser.parse_args()

    # Instantiate the LipNet model.
    model = LipNet()

    # Load the checkpoint.
    checkpoint = torch.load(args.checkpoint, map_location=torch.device("cpu"))

    # If the checkpoint contains a "model_state_dict" key, extract it.
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
    else:
        state_dict = checkpoint

    # Load the model weights.
    model.load_state_dict(state_dict)
    model.eval()  # Set model to evaluation mode

    # Create a dummy input tensor with the expected shape: (batch, channels, T, H, W)
    dummy_input = torch.randn(1, 3, 75, 50, 100)

    # Export the model to ONNX format.
    torch.onnx.export(
        model,                      # model being exported
        dummy_input,                # dummy input tensor
        args.output,                # output file path
        export_params=True,         # store the trained parameter weights inside the model file
        opset_version=11,           # ONNX version to export the model to
        input_names=["input"],      # model input name
        output_names=["output"],    # model output name
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"}
        }                           # support variable batch size
    )

    print(f"LipNet model has been successfully exported to {args.output}")

if __name__ == "__main__":
    main()



# python machine_learning/scripts/convert_pth_to_onnx.py --checkpoint=machine_learning/checkpoints/lipnet_epoch_100.pth --output machine_learning/lipseek_onnx_model.onnx