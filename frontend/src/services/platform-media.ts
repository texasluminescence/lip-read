import { Platform } from 'react-native';
import * as MediaLibrary from 'expo-media-library';
import * as DocumentPicker from 'expo-document-picker';
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
  
  console.log('Checking media library permissions...');
  
  // First check if we have permissions with full detail
  const permissionInfo = await MediaLibrary.getPermissionsAsync();
  console.log('Current permission status:', JSON.stringify(permissionInfo));
  
  if (permissionInfo.status !== 'granted') {
    console.log('Requesting media library permissions...');
    const newPermissionInfo = await MediaLibrary.requestPermissionsAsync();
    console.log('New permission status:', JSON.stringify(newPermissionInfo));
    
    if (newPermissionInfo.status !== 'granted') {
      console.log('Media library permission was denied');
      return { assets: [] };
    }
  }
  
  try {
    console.log('Getting videos from media library...');
    
    // Get all video assets from the media library
    const results = await MediaLibrary.getAssetsAsync({
      mediaType: MediaLibrary.MediaType.video,
      sortBy: [MediaLibrary.SortBy.creationTime],
      first: 100, // Increased to 100 videos
    });

    console.log(`Found ${results.assets.length} videos in library`);
    
    if (results.assets.length === 0) {
      console.log('No videos found in library, trying with broader criteria...');
      
      // Try with a broader query as fallback
      const allMediaResults = await MediaLibrary.getAssetsAsync({
        first: 100,
      });
      
      // Filter for video types based on extension
      const potentialVideos = allMediaResults.assets.filter(asset => {
        const filename = asset.filename.toLowerCase();
        return filename.endsWith('.mp4') || 
               filename.endsWith('.mov') || 
               filename.endsWith('.3gp') ||
               filename.endsWith('.avi') ||
               filename.endsWith('.mkv');
      });
      
      console.log(`Found ${potentialVideos.length} potential videos by extension filtering`);
      
      if (potentialVideos.length > 0) {
        return { assets: potentialVideos };
      }
    }
    
    return results;
  } catch (error) {
    console.error('Error loading videos from media library:', error);
    return { assets: [] };
  }
};

// Select a video file from device using document picker
export const selectVideoFromLibrary = async (): Promise<string | null> => {
  if (Platform.OS === 'web') {
    try {
      return await pickVideoFromLibrary();
    } catch (error) {
      console.error('Error picking video:', error);
      return null;
    }
  }
  
  // On mobile platforms, use the document picker
  try {
    const result = await DocumentPicker.getDocumentAsync({
      type: 'video/*',
      copyToCacheDirectory: true, // Copy file to app's cache for reliable access
    });
    
    if (result.canceled) {
      console.log('Document picker was canceled');
      return null;
    }
    
    // DocumentPicker now returns an array of assets, so we take the first one
    if (result.assets && result.assets.length > 0) {
      console.log('Selected video file:', result.assets[0].uri);
      return result.assets[0].uri;
    }
    
    return null;
  } catch (error) {
    console.error('Error picking document:', error);
    return null;
  }
};