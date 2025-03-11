import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from model.inference_wrapper import get_prediction

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/', methods=['GET'])
def index():
    return "Lipreading Model API is running!"

@predict_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded video to a temporary file.
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        file.save(tmp)
        temp_path = tmp.name

    try:
        prediction = get_prediction(temp_path)
    except Exception as e:
        os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

    os.remove(temp_path)
    return jsonify({'prediction': prediction})
