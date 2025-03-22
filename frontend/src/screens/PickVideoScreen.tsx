import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, FlatList, Image, TouchableOpacity, ActivityIndicator, Platform } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/navigation';
import * as VideoThumbnails from 'expo-video-thumbnails';
import { checkMediaLibraryPermissions, getVideosFromLibrary, selectVideoFromLibrary } from '../services/platform-media';

type PickVideoScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'PickVideo'>;

interface VideoAsset extends MediaLibrary.Asset {
  thumbnailUri?: string;
}

const PickVideoScreen: React.FC = () => {
  const navigation = useNavigation<PickVideoScreenNavigationProp>();
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [videos, setVideos] = useState<VideoAsset[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      // Special case for web platform - show a button to pick a file instead of library
      if (Platform.OS === 'web') {
        setHasPermission(true);
        setLoading(false);
        return;
      }
      
      const granted = await checkMediaLibraryPermissions();
      setHasPermission(granted);
      
      if (granted) {
        loadVideos();
      } else {
        setLoading(false);
      }
    })();
  }, []);

  const loadVideos = async () => {
    // Skip this on web platform
    if (Platform.OS === 'web') return;
    
    try {
      const media = await getVideosFromLibrary();
      
      // Get thumbnails for videos
      const videosWithThumbnails: VideoAsset[] = await Promise.all(
        media.assets.map(async (video) => {
          try {
            const { uri } = await VideoThumbnails.getThumbnailAsync(video.uri, {
              time: 0,
              quality: 0.5,
            });
            return { ...video, thumbnailUri: uri };
          } catch (e) {
            return { ...video };
          }
        })
      );
      
      setVideos(videosWithThumbnails);
    } catch (error) {
      console.error('Error loading videos:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Web file picker handler
  const handleWebFilePicker = async () => {
    if (Platform.OS !== 'web') return;
    
    try {
      const uri = await selectVideoFromLibrary();
      if (uri) {
        navigation.navigate('Preview', { uri });
      }
    } catch (error) {
      console.error('Error picking file:', error);
    }
  };

  const handleSelectVideo = (video: VideoAsset) => {
    navigation.navigate('Preview', { uri: video.uri });
  };

  if (hasPermission === null) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#4285F4" />
      </View>
    );
  }

  if (hasPermission === false) {
    return (
      <View style={styles.center}>
        <Text style={styles.noPermissionText}>
          LipSeek needs access to your media library to select videos.
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />
      
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <MaterialIcons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        <Text style={styles.title}>Select Video</Text>
      </View>
      
      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color="#4285F4" />
        </View>
      ) : Platform.OS === 'web' ? (
        <View style={styles.center}>
          <TouchableOpacity style={styles.webPickButton} onPress={handleWebFilePicker}>
            <MaterialIcons name="upload-file" size={48} color="#4285F4" />
            <Text style={styles.webPickButtonText}>Select a video file</Text>
          </TouchableOpacity>
        </View>
      ) : videos.length === 0 ? (
        <View style={styles.center}>
          <Text style={styles.noVideosText}>No videos found</Text>
        </View>
      ) : (
        <FlatList
          data={videos}
          numColumns={2}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <TouchableOpacity 
              style={styles.videoItem}
              onPress={() => handleSelectVideo(item)}
            >
              {item.thumbnailUri ? (
                <Image 
                  source={{ uri: item.thumbnailUri }}
                  style={styles.thumbnail}
                />
              ) : (
                <View style={[styles.thumbnail, styles.placeholderThumbnail]}>
                  <MaterialIcons name="videocam" size={40} color="#999" />
                </View>
              )}
              <Text style={styles.duration}>
                {formatDuration(item.duration)}
              </Text>
            </TouchableOpacity>
          )}
        />
      )}
    </View>
  );
};

// Helper function to format video duration
const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    paddingTop: 50,
    backgroundColor: 'white',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  backButton: {
    marginRight: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  videoItem: {
    flex: 1,
    margin: 8,
    borderRadius: 8,
    overflow: 'hidden',
    backgroundColor: 'white',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
  },
  thumbnail: {
    width: '100%',
    aspectRatio: 16 / 9,
  },
  placeholderThumbnail: {
    backgroundColor: '#eee',
    justifyContent: 'center',
    alignItems: 'center',
  },
  duration: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    color: 'white',
    padding: 4,
    borderRadius: 4,
    fontSize: 12,
  },
  noPermissionText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  noVideosText: {
    fontSize: 16,
    color: '#666',
  },
  webPickButton: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    width: 250,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 3,
  },
  webPickButtonText: {
    marginTop: 16,
    fontSize: 16,
    color: '#333',
    fontWeight: 'bold',
  },
});

export default PickVideoScreen;