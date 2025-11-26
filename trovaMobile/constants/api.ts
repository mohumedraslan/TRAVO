import { Platform } from 'react-native';

// Base API configuration
export const API_CONFIG = {
  // For Android emulator, use 10.0.2.2 to access host machine's localhost
  // For iOS simulator and physical devices, use your machine's local IP
  // For web, use localhost or your machine's IP
  BASE_URL: Platform.select({
    android: 'http://192.168.1.5:8001',
    ios: 'http://localhost:8001',
    default: 'http://localhost:8001',
  }),

  // API endpoints
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      REFRESH: '/auth/refresh',
    },
    LANDMARKS: {
      DETECT: '/landmarks/detect',
      SEARCH: '/landmarks/search',
      DETAILS: '/landmarks/',
    },
    ITINERARY: {
      CREATE: '/itinerary',
      GET: '/itinerary/',
      UPDATE: '/itinerary/',
      DELETE: '/itinerary/',
    },
  },

  // Timeout for API requests (in milliseconds)
  TIMEOUT: 30000,

  // Default headers
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
};

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${API_CONFIG.BASE_URL}/${cleanEndpoint}`;
};

export default API_CONFIG;
