import client from './client';

export interface IdentifyResponse {
  identified_monument: string;
  confidence: number;
}

export const identifyMonument = async (imageUri: string): Promise<IdentifyResponse> => {
  const formData = new FormData();
  formData.append('file', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'monument.jpg',
  } as any);

  const response = await client.post(`/vision/identify`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};