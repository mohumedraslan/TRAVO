import { Platform } from 'react-native';
import Constants from 'expo-constants';

// Default to localhost for web and iOS, 10.0.2.2 for Android emulator
const LOCAL_IP = '192.168.1.5'; // Change this to your local IP if testing on physical device
const LOCAL_BACKEND_URL = `http://${LOCAL_IP}:8000`;
const EMULATOR_BACKEND_URL = 'http://192.168.1.5:8001';

// Determine the base URL based on platform
export const getBaseUrl = () => {
  // In production, use the production URL
  if (process.env.NODE_ENV === 'production') {
    return 'https://your-production-api.com';
  }

  // For web, use localhost
  if (Platform.OS === 'web') {
    return 'http://localhost:8000';
  }

  // For Android emulator
  if (Platform.OS === 'android') {
    return EMULATOR_BACKEND_URL;
  }

  // For iOS simulator or physical device
  return LOCAL_BACKEND_URL;
};

export const API_BASE_URL = getBaseUrl();

// Log the API URL being used
console.log(`[API] Using base URL: ${API_BASE_URL} (Platform: ${Platform.OS})`);
