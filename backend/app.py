from flask import Flask
from flask_socketio import SocketIO
from routes.predict import predict_bp
from routes.socket import socketio  # import the SocketIO instance from socket.py

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(predict_bp)
    socketio.init_app(app, cors_allowed_origins="*")
    return app
    
if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000)
