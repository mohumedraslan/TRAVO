import axios from 'axios';
import Constants from 'expo-constants';

// Function to get the API base URL from environment variables
const getApiBaseUrl = (): string => {
  // Access environment variables via expo-constants
  const env = Constants.expoConfig?.extra;

  // Check for a specific API URL in the environment config
  if (env?.API_URL) {
    return env.API_URL;
  }

  // Fallback for development environments
  // Note: For Android emulators, you may need to use 'http://10.0.2.2:8000/api'
  // For physical devices, you'll need to use your machine's local network IP.
  return process.env.NODE_ENV === 'production'
    ? 'https://your-production-api-domain.com/api' // Replace with your actual production URL
    : 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
});

export default client;
