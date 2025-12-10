import axios from 'axios';
import { Platform } from 'react-native';

// YOUR PC's LOCAL IP ADDRESS
// Find it by running: ipconfig (Windows) or ifconfig (Mac/Linux)
// Make sure phone is on the same WiFi network!
const LOCAL_NETWORK_IP = '192.168.1.5';

// Determine the base URL based on platform
const getBaseUrl = () => {
  if (Platform.OS === 'android') {
    // For physical Android device - use your PC's local IP
    // For Android Emulator, use 10.0.2.2 instead
    return `http://${LOCAL_NETWORK_IP}:8000/api`;
  } else if (Platform.OS === 'ios') {
    // iOS Simulator can use localhost
    return 'http://localhost:8000/api';
  } else {
    // Web
    return 'http://localhost:8000/api';
  }
};

const client = axios.create({
  baseURL: getBaseUrl(),
  timeout: 60000, // 60 seconds for vision API which can be slow
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
