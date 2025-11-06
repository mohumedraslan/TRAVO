import axios from 'axios';
import { Platform } from 'react-native';

// Configure API base URL based on platform
const API_BASE_URL = Platform.OS === 'android' 
  ? 'http://10.0.2.2:8000' 
  : 'http://localhost:8000';

console.log(`[API] Using base URL: ${API_BASE_URL}`);

// Create axios instance with default config
const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000, // 15 seconds timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // Important for sessions/cookies
});

// Request interceptor
client.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
    });
    
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
client.interceptors.response.use(
  (response) => {
    console.log(`[API] ${response.status} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    const errorMessage = {
      message: error.message,
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method,
      response: error.response?.data,
    };
    
    console.error('[API] Response error:', errorMessage);
    
    // Handle specific status codes
    if (error.response?.status === 401) {
      // Handle unauthorized (e.g., redirect to login)
      console.warn('[API] Unauthorized - redirecting to login');
      // Add your auth redirect logic here
    }
    
    return Promise.reject({
      ...error,
      message: error.response?.data?.message || error.message,
      status: error.response?.status,
    });
  }
);

// Helper functions for common API operations
export const api = {
  get: (url: string, config = {}) => client.get(url, config),
  post: (url: string, data: any, config = {}) => client.post(url, data, config),
  put: (url: string, data: any, config = {}) => client.put(url, data, config),
  delete: (url: string, config = {}) => client.delete(url, config),
  patch: (url: string, data: any, config = {}) => client.patch(url, data, config),
};

export default client;
