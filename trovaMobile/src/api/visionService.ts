import client from './client';

export interface IdentifyResponse {
  identified_monument: string;
  confidence: number;
}

export const identifyMonument = async (imageUri: string): Promise<IdentifyResponse | null> => {
  const formData = new FormData();
  // Backend expects field name 'image' per FastAPI route
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'monument.jpg',
  } as any);

  const response = await client.post(`/vision/identify`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};