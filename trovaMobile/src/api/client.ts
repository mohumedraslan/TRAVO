import axios from 'axios';
import Constants from 'expo-constants';

const API_BASE = (Constants?.expoConfig?.extra as any)?.API_URL || 'http://127.0.0.1:8000/api';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

export default client;
