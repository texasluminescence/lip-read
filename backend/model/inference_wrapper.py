from vtp_lipreading import inference  
from vtp_lipreading.config import load_args 
from importlib_resources import files

# Initialize your model and related components only once.
def init_model():
    # Create args from your package's config.
    args = load_args()
    # You can set default checkpoint paths if needed.
    args.ckpt_path = str(files('vtp_lipreading').joinpath('checkpoints', 'ft_lrs3.pth'))
    args.cnn_ckpt_path = str(files('vtp_lipreading').joinpath('feature_extractors', 'feature_extractor.pth'))
    args.builder = 'vtp24x24'
    args.beam_size = 30
    args.max_decode_len = 35
    # Initialize inference (this calls main() from inference.py)
    model, video_loader, lm, lm_tokenizer = inference.main(args)
    return model, video_loader, lm, lm_tokenizer

# Initialize the model at module level.
_model, _video_loader, _lm, _lm_tokenizer = init_model()

def get_prediction(video_path):
    """
    Given a path to a video file, run inference using the lipreading model and return the predicted text.
    """
    # 'run' is imported from vtp_lipreading.inference module
    prediction = inference.run(
        video_path, _video_loader, _model, _lm, _lm_tokenizer, display=False
    )
    return prediction
