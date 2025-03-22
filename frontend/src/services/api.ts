import axios from 'axios';
import { Platform } from 'react-native';

// Use HTTPS for web platform
const API_URL = Platform.OS === 'web' 
  ? 'https://api.dermetric.cashel.dev:5555'
  : 'http://api.dermetric.cashel.dev:5555';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const uploadVideo = async (videoUri: string): Promise<string> => {
  try {
    const formData = new FormData();
    
    if (Platform.OS === 'web') {
      // For web, we need to fetch the blob from the URL
      if (videoUri.startsWith('blob:')) {
        const response = await fetch(videoUri);
        const blob = await response.blob();
        const fileType = 'webm';
        const fileName = `video-${Date.now()}.${fileType}`;
        formData.append('file', blob, fileName);
      } else {
        throw new Error('Invalid video URI format for web');
      }
    } else {
      // Native platform handling
      const fileType = videoUri.split('.').pop() || 'mp4';
      const fileName = `video-${Date.now()}.${fileType}`;
      
      // @ts-ignore: FormData in React Native works differently
      formData.append('file', {
        uri: videoUri,
        name: fileName,
        type: `video/${fileType}`,
      });
    }

    const response = await api.post('/predict', formData);
    return response.data.prediction;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
};

export default api;