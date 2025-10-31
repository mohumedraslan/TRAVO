import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface IdentifyResponse {
  identified_monument: string;
  description: string;
  confidence: number;
}

export const identifyMonument = async (imageUri: string): Promise<IdentifyResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'monument.jpg',
    } as any);

    const response = await axios.post(`${API_URL}/vision/identify`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error identifying monument:', error);
    throw error;
  }
};