import base64
import os
import tempfile
import cv2
import numpy as np
from flask_socketio import SocketIO, emit
from model.inference_wrapper import get_prediction

# Create a SocketIO instance.
socketio = SocketIO(cors_allowed_origins="*")

# Global frame buffer to accumulate video frames.
frame_buffer = []

@socketio.on('connect')
def handle_connect():
    print("Client connected via WebSocket")
    emit('response', {'message': 'Connected to Lipreading WebSocket'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('video_frame')
def handle_video_frame(data):
    """
    Expecting data as a dictionary with a key 'frame' containing a base64-encoded image.
    """
    try:
        frame_data = data.get('frame')
        if not frame_data:
            emit('error', {'message': 'No frame data provided'})
            return

        # Decode the base64 frame data into an image using OpenCV.
        img_bytes = base64.b64decode(frame_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_buffer.append(img)

        # Process when buffer reaches 30 frames (adjust threshold as needed).
        if len(frame_buffer) >= 30:
            # Create a temporary video file.
            temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            temp_video_path = temp_video.name
            temp_video.close()
            
            # Get frame dimensions.
            height, width, _ = frame_buffer[0].shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_video_path, fourcc, 25, (width, height))
            
            # Write frames into the video file.
            for frame in frame_buffer:
                out.write(frame)
            out.release()

            # Run inference on the temporary video file.
            transcript = get_prediction(temp_video_path)
            
            # Clean up temporary file and reset buffer.
            os.remove(temp_video_path)
            frame_buffer.clear()

            # Emit the transcript back to the client.
            emit('transcript', {'text': transcript})
        else:
            # Optionally, acknowledge receipt of the frame.
            emit('response', {'message': f'Received frame. Buffer size: {len(frame_buffer)}'})
    except Exception as e:
        emit('error', {'message': str(e)})
