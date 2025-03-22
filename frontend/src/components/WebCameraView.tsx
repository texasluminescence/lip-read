import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, View, TouchableOpacity, Text, Platform } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

interface WebCameraViewProps {
  onVideoRecorded: (uri: string) => void;
}

const WebCameraView: React.FC<WebCameraViewProps> = ({ onVideoRecorded }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null);
  const [videoURL, setVideoURL] = useState<string | null>(null);
  const [isCameraAvailable, setIsCameraAvailable] = useState(true);
  const [facingMode, setFacingMode] = useState('user'); // 'user' for front camera, 'environment' for back
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const chunks = useRef<Blob[]>([]);

  // Start the camera when component mounts
  useEffect(() => {
    setupCamera();
    
    // Cleanup when component unmounts
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [facingMode]);

  const setupCamera = async () => {
    try {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
      
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode
        },
        audio: true
      });
      
      setCameraStream(stream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      
      setIsCameraAvailable(true);
    } catch (error) {
      console.error('Error accessing camera:', error);
      setIsCameraAvailable(false);
    }
  };

  const toggleCameraFacing = () => {
    setFacingMode(current => (current === 'environment' ? 'user' : 'environment'));
  };

  const prepareRecording = () => {
    startRecording();
  };

  const startRecording = async () => {
    if (!cameraStream) return;
    
    chunks.current = [];
    setIsRecording(true);
    
    try {
      const recorder = new MediaRecorder(cameraStream);
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.current.push(event.data);
        }
      };
      
      recorder.onstop = () => {
        const blob = new Blob(chunks.current, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        setVideoURL(url);
        onVideoRecorded(url);
        setIsRecording(false);
      };
      
      setMediaRecorder(recorder);
      recorder.start();
      
      // Auto stop after 10 seconds (can be adjusted)
      setTimeout(() => {
        if (recorder.state === 'recording') {
          stopRecording();
        }
      }, 10000);
    } catch (error) {
      console.error('Error starting recording:', error);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  if (!isCameraAvailable) {
    return (
      <View style={styles.container}>
        <Text style={{color: 'white'}}>Camera not available or permission denied</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <video 
        ref={videoRef} 
        style={styles.camera} 
        autoPlay 
        playsInline 
        muted 
      />
      <View style={styles.controlsContainer}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.iconButton}
            onPress={toggleCameraFacing}
            disabled={isRecording}
          >
            <MaterialIcons name="flip-camera-ios" size={36} color="white" />
          </TouchableOpacity>
          {isRecording ? (
            <TouchableOpacity
              style={[styles.recordButton, styles.recordingButton]}
              onPress={stopRecording}
            />
          ) : (
            <TouchableOpacity
              style={styles.recordButton}
              onPress={prepareRecording}
              disabled={isRecording}
            />
          )}
          <View style={styles.iconButton} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  camera: {
    flex: 1,
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  controlsContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'transparent',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    marginBottom: 30,
  },
  recordButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'red',
    borderWidth: 5,
    borderColor: 'white',
  },
  recordingButton: {
    backgroundColor: 'white',
    borderWidth: 20,
    borderColor: 'red',
  },
  iconButton: {
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default WebCameraView;