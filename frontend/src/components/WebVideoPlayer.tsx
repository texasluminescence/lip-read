import React, { useRef, useEffect } from 'react';
import { StyleSheet, View } from 'react-native';

interface WebVideoPlayerProps {
  uri: string;
  style?: any;
}

const WebVideoPlayer: React.FC<WebVideoPlayerProps> = ({ uri, style }) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.src = uri;
    }
  }, [uri]);

  return (
    <View style={[styles.container, style]}>
      <video 
        ref={videoRef}
        style={styles.video}
        controls
        playsInline
        autoPlay
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    overflow: 'hidden',
    borderRadius: 10,
  },
  video: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
});

export default WebVideoPlayer;