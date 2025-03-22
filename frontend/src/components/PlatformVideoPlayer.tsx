import React from 'react';
import { Platform } from 'react-native';
import VideoPlayer from './VideoPlayer';
import WebVideoPlayer from './WebVideoPlayer';

interface PlatformVideoPlayerProps {
  uri: string;
  style?: any;
}

const PlatformVideoPlayer: React.FC<PlatformVideoPlayerProps> = (props) => {
  if (Platform.OS === 'web') {
    return <WebVideoPlayer {...props} />;
  }
  
  return <VideoPlayer {...props} />;
};

export default PlatformVideoPlayer;