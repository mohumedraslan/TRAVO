import * as FileSystem from 'expo-file-system/legacy';
import { api } from '../api/client';
import client from '../api/client';

export interface MonumentDetectionResult {
  monumentName: string;
  confidence: number;
  description?: string;
  location?: string;
  top3?: Array<{
    monumentName: string;
    confidence: number;
  }>;
}

export const detectMonument = async (imageUri: string): Promise<MonumentDetectionResult> => {
  try {
    console.log(`[MonumentService] Starting monument detection for image: ${imageUri}`);
    console.log(`[MonumentService] API Base URL: ${client.defaults.baseURL}`);
    
    // Read the image file as base64
    const base64 = await FileSystem.readAsStringAsync(imageUri, {
      encoding: 'base64',
    });
    
    console.log(`[MonumentService] Image converted to base64, length: ${base64.length}`);
    
    // Send to backend for detection
    const response = await api.post('/vision/identify', {
      image: base64,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds for model inference
    });
    
    console.log(`[MonumentService] Detection result:`, JSON.stringify(response.data, null, 2));
    
    // Parse the new backend response format
    const data = response.data;
    const candidates = data.candidates || [];
    
    // Return the detection result with top-3 predictions
    return {
      monumentName: data.identified_monument || 'Unknown',
      confidence: data.confidence || 0,
      description: data.description,
      location: data.location,
      top3: candidates.map((c: any) => ({
        monumentName: c.monument_name,
        confidence: c.confidence
      })),
    };
  } catch (error: any) {
    console.error('[MonumentService] Error detecting monument:', error);
    console.error('[MonumentService] Error response:', error.response?.data);
    console.error('[MonumentService] Error status:', error.response?.status);
    
    // Provide more specific error messages
    if (error.response?.status === 404) {
      throw new Error('Monument detection endpoint not found. Please check your backend configuration.');
    } else if (error.response?.status === 500) {
      throw new Error('Server error during monument detection. Please try again.');
    } else if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      throw new Error('Detection timed out. Please try with a smaller image.');
    } else if (error.code === 'ERR_NETWORK') {
      throw new Error('Cannot connect to server. Please check your network connection.');
    }
    
    throw new Error('Failed to detect monument. Please try again.');
  }
};

export const getMonumentInfo = async (monumentName: string) => {
  try {
    // In a real app, this would fetch from your backend
    const mockInfo = {
      name: monumentName,
      description: 'This is a detailed description of ' + monumentName,
      history: 'Historical information about ' + monumentName,
      location: 'Location of ' + monumentName,
      // Add more fields as needed
    };
    
    return mockInfo;
  } catch (error) {
    console.error('[MonumentService] Error getting monument info:', error);
    throw error;
  }
};
