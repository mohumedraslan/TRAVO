import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

const extra = (Constants?.expoConfig?.extra as any) || {};
let API_BASE: string = extra.API_URL || 'http://127.0.0.1:8000/api';

// Fix localhost resolution for Android emulator and common cases
if (Platform.OS === 'android') {
  if (API_BASE.includes('127.0.0.1')) {
    API_BASE = API_BASE.replace('127.0.0.1', '10.0.2.2');
  }
  if (API_BASE.includes('localhost')) {
    API_BASE = API_BASE.replace('localhost', '10.0.2.2');
  }
}

const client = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

export default client;
