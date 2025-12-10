import axios from 'axios';

import { Platform } from 'react-native';

// Use 10.0.2.2 for Android Emulator, local IP for physical device, localhost for iOS Sim/Web
// IMPORTANT: If running on a physical device over WiFi, use your computer's local IP (e.g., 192.168.1.5)
const LOCAL_NETWORK_IP = '192.168.1.5'; // Change this to your PC's IP

const API_URL = Platform.select({
  android: `http://${LOCAL_NETWORK_IP}:8000/api`, // Use local IP for physical device
  ios: 'http://localhost:8000/api',
  default: 'http://localhost:8000/api',
});

const client = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

export default client;
