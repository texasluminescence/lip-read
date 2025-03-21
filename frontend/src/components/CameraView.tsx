import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import {
  CameraView as ExpoCameraView,
  CameraType,
  useCameraPermissions,
} from "expo-camera";
import { MaterialIcons } from '@expo/vector-icons';

interface CameraViewProps {
  onVideoRecorded: (uri: string) => void;
}

const CameraView: React.FC<CameraViewProps> = ({ onVideoRecorded }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [facing, setFacing] = useState<CameraType>('front');
  const cameraRef = useRef<ExpoCameraView>(null);

  // Use the hook to handle permissions.
  const [permission, requestPermission] = useCameraPermissions();

  useEffect(() => {
    if (!permission) return; // Permission still loading
    if (!permission.granted) {
      requestPermission();
    }
  }, [permission]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (countdown !== null && countdown > 0) {
      interval = setInterval(() => {
        setCountdown(prev => (prev !== null ? prev - 1 : null));
      }, 1000);
    } else if (countdown === 0) {
      setCountdown(null);
      startRecording();
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [countdown]);

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  };

  const prepareRecording = () => {
    setCountdown(3);
  };

  const startRecording = async () => {
    if (cameraRef.current) {
      setIsRecording(true);
      try {
        const video = await cameraRef.current?.recordAsync();
        setIsRecording(false);
        if (!video) {
          setIsRecording(false);
          console.error("Recording failed: video is undefined.");
          return;
        }
        onVideoRecorded(video.uri);
      } catch (error) {
        console.error('Error recording video:', error);
        setIsRecording(false);
      }
    }
  };

  const stopRecording = async () => {
    if (cameraRef.current && isRecording) {
      cameraRef.current?.stopRecording();
      setIsRecording(false);
    }
  };

  if (!permission) {
    return (
      <View style={styles.container}>
        <Text>Loading permissions...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text>No access to camera</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ExpoCameraView ref={cameraRef} style={styles.camera} facing={facing} mode="video">
        <View style={styles.controlsContainer}>
          {countdown !== null && (
            <View style={styles.countdownContainer}>
              <Text style={styles.countdownText}>{countdown}</Text>
            </View>
          )}
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
                disabled={countdown !== null}
              />
            )}
            <View style={styles.iconButton} />
          </View>
        </View>
      </ExpoCameraView>
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
  },
  controlsContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    justifyContent: 'flex-end',
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
  countdownContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  countdownText: {
    fontSize: 100,
    color: 'white',
    fontWeight: 'bold',
  },
});

export default CameraView;