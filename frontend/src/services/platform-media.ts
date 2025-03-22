import { Platform } from 'react-native';
import * as MediaLibrary from 'expo-media-library';
import { pickVideoFromLibrary } from './web-file-picker';

// Check media library permissions on native platforms
export const checkMediaLibraryPermissions = async (): Promise<boolean> => {
  if (Platform.OS === 'web') {
    return true; // Web doesn't need permissions for file picker
  }
  
  const { status } = await MediaLibrary.requestPermissionsAsync();
  return status === 'granted';
};

// Get videos from media library
export const getVideosFromLibrary = async () => {
  if (Platform.OS === 'web') {
    // Web platforms don't have a media library API, so we return an empty array
    // The web implementation will use a file picker instead
    return { assets: [] };
  }
  
  return await MediaLibrary.getAssetsAsync({
    mediaType: MediaLibrary.MediaType.video,
    sortBy: [MediaLibrary.SortBy.creationTime],
  });
};

// Select a video from device
export const selectVideoFromLibrary = async (): Promise<string | null> => {
  if (Platform.OS === 'web') {
    try {
      return await pickVideoFromLibrary();
    } catch (error) {
      console.error('Error picking video:', error);
      return null;
    }
  }
  
  // This function should be implemented for native platforms if needed
  // For now, we'll return null since native platforms use the PickVideoScreen component
  return null;
};