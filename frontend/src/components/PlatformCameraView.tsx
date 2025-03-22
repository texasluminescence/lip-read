import React from 'react';
import { Platform } from 'react-native';
import CameraView from './CameraView';
import WebCameraView from './WebCameraView';

interface PlatformCameraViewProps {
  onVideoRecorded: (uri: string) => void;
}

const PlatformCameraView: React.FC<PlatformCameraViewProps> = (props) => {
  if (Platform.OS === 'web') {
    return <WebCameraView {...props} />;
  }
  
  return <CameraView {...props} />;
};

export default PlatformCameraView;