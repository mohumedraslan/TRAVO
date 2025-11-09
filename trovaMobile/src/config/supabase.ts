import { createClient } from '@supabase/supabase-js';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use the correct storage key based on platform
const storageKey = 'supabase.auth.token';

// Create a custom storage adapter
const storage = {
  getItem: (key: string) => {
    return AsyncStorage.getItem(key);
  },
  setItem: (key: string, value: string) => {
    return AsyncStorage.setItem(key, value);
  },
  removeItem: (key: string) => {
    return AsyncStorage.removeItem(key);
  },
};

// Initialize the Supabase client with the configuration
const supabaseUrl = 'https://mvqljubjlufjyyktsljn.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA';

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: storage as any,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: Platform.OS === 'web',
  },
});

// Add a function to handle auth state changes
supabase.auth.onAuthStateChange((event, session) => {
  console.log('Auth state changed:', event, session);
});

export default supabase;
