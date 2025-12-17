import axios from 'axios';
import { Platform } from 'react-native';
import { API_URL } from '../config';

const client = axios.create({
  baseURL: API_URL,
  timeout: 120000, // 120 seconds for vision API (increased for safety)
  headers: {
    'Accept': 'application/json',
  }
});

// Request interceptor for debugging
client.interceptors.request.use(
  (config) => {
    console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('📡 Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging
client.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} from ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(`❌ API Error: ${error.message}`);
    if (error.response) {
      console.error(`   Status: ${error.response.status}`);
      console.error(`   Data: ${JSON.stringify(error.response.data)}`);
    } else if (error.request) {
      console.error('   No response received - check if backend is running');
      console.error(`   URL: ${error.config?.baseURL}${error.config?.url}`);
    }
    return Promise.reject(error);
  }
);

export default client;
