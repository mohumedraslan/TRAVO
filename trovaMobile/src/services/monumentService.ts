// import * as FileSystem from 'expo-file-system';
// import * as ImageManipulator from 'expo-image-manipulator';
// import { api } from '../api/client';

export interface MonumentDetectionResult {
  monumentName: string;
  confidence: number;
  description?: string;
  location?: string;
}

export const detectMonument = async (imageUri: string): Promise<MonumentDetectionResult> => {
  try {
    console.log(`[MonumentService] Starting monument detection for image: ${imageUri}`);
    
    // For demo purposes, we'll use a mock response
    // In a real app, you would send the image to your backend
    const mockMonuments: MonumentDetectionResult[] = [
      { 
        monumentName: 'The Great Pyramid of Giza', 
        confidence: 0.95, 
        description: 'The last remaining wonder of the ancient world', 
        location: 'Giza, Egypt' 
      },
      { 
        monumentName: 'The Sphinx', 
        confidence: 0.92, 
        description: 'A limestone statue of a reclining sphinx', 
        location: 'Giza, Egypt' 
      },
      { 
        monumentName: 'Karnak Temple', 
        confidence: 0.88, 
        description: 'Vast temple complex in Luxor', 
        location: 'Luxor, Egypt' 
      },
    ];
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Return a random monument for demo
    const randomIndex = Math.floor(Math.random() * mockMonuments.length);
    return mockMonuments[randomIndex];
    
    // Uncomment this in production to use the real API
    /*
    // Prepare the image for upload
    const resizedImage = await ImageManipulator.manipulateAsync(
      imageUri,
      [{ resize: { width: 800 } }],
      { compress: 0.8, format: ImageManipulator.SaveFormat.JPEG, base64: true }
    );

    const formData = new FormData();
    formData.append('image', {
      uri: imageUri,
      name: 'monument.jpg',
      type: 'image/jpeg',
      data: resizedImage.base64,
    } as any);

    const response = await api.post('/vision/identify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
    */
  } catch (error) {
    console.error('[MonumentService] Error detecting monument:', error);
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
