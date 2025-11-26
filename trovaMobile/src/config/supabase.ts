import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use the correct storage key based on platform
const storageKey = 'supabase.auth.token';

// Create a custom storage adapter that handles errors gracefully
const storage = {
  getItem: async (key: string) => {
    try {
      if (Platform.OS === 'web' && typeof window === 'undefined') {
        return null;
      }
      return await AsyncStorage.getItem(key);
    } catch (error) {
      console.warn('Supabase storage getItem error:', error);
      return null;
    }
  },
  setItem: async (key: string, value: string) => {
    try {
      if (Platform.OS === 'web' && typeof window === 'undefined') {
        return;
      }
      await AsyncStorage.setItem(key, value);
    } catch (error) {
      console.warn('Supabase storage setItem error:', error);
    }
  },
  removeItem: async (key: string) => {
    try {
      if (Platform.OS === 'web' && typeof window === 'undefined') {
        return;
      }
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.warn('Supabase storage removeItem error:', error);
    }
  },
};

// Initialize the Supabase client with the configuration
const supabaseUrl = 'https://mvqljubjlufjyyktsljn.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA';

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: storage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: Platform.OS === 'web',
  },
});

// Add a function to handle auth state changes
supabase.auth.onAuthStateChange((event, session) => {
  // console.log('Auth state changed:', event, session);
});

export default supabase;
