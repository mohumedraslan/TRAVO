import React from 'react';
import LoginScreen from '@/src/screens/LoginScreen';

export default function HomeTab() {
  return <LoginScreen navigation={{ navigate: () => {}, replace: () => {} }} />;
}
