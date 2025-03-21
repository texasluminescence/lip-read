import axios from 'axios';

const API_URL = 'http://api.dermetric.cashel.dev:5555';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const uploadVideo = async (videoUri: string): Promise<string> => {
  try {
    const formData = new FormData();
    
    // Create file object from URI
    const fileType = videoUri.split('.').pop() || 'mp4';
    const fileName = `video-${Date.now()}.${fileType}`;
    
    // @ts-ignore: FormData in React Native works differently
    formData.append('file', {
      uri: videoUri,
      name: fileName,
      type: `video/${fileType}`,
    });

    const response = await api.post('/predict', formData);
    return response.data.prediction;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
};

export default api;