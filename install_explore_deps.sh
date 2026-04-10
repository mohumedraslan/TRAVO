#!/bin/bash

# Navigate to the mobile app directory
cd trovaMobile

# Install required dependencies
echo "Installing required dependencies for ExploreScreen..."
npm install @react-navigation/stack @react-navigation/native react-native-screens react-native-safe-area-context @expo/vector-icons

# Install type definitions for TypeScript
npx expo install @types/react @types/react-native @types/react-navigation @types/react-navigation-stack

echo "Dependencies installed successfully!"
echo "Please restart your development server for the changes to take effect."
