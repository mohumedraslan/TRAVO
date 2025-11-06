import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

const extra = (Constants?.expoConfig?.extra as any) || {};
let API_BASE: string = extra.API_URL || 'http://localhost:8000/api';

// Platform-specific API base URL configuration
if (Platform.OS === 'android') {
  // Android emulator needs 10.0.2.2 to access host machine
  if (API_BASE.includes('127.0.0.1') || API_BASE.includes('localhost')) {
    API_BASE = API_BASE.replace('127.0.0.1', '10.0.2.2').replace('localhost', '10.0.2.2');
  }
} else if (Platform.OS === 'web') {
  // Web can use localhost directly
  API_BASE = 'http://localhost:8000/api';
}

console.log(`[API Client] Using API base URL: ${API_BASE} (Platform: ${Platform.OS})`);

const client = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add request interceptor for debugging
client.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
client.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error(`[API Error] ${error.response.status} ${error.config?.url}`, error.response.data);
    } else if (error.request) {
      console.error('[API Network Error] No response received', error.message);
    } else {
      console.error('[API Error]', error.message);
    }
    return Promise.reject(error);
  }
);

export default client;
