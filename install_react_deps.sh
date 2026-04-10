#!/bin/bash

# Navigate to the mobile app directory
cd trovaMobile

# Install required dependencies
echo "Installing React and React Native dependencies..."
npm install react@^18.2.0 react-native@0.72.0 @types/react@^18.2.0 @types/react-native@^0.72.0

# Install navigation dependencies
npm install @react-navigation/native @react-navigation/stack react-native-screens react-native-safe-area-context

# Install vector icons
npm install @expo/vector-icons

# Install type definitions
echo "Installing type definitions..."
npx expo install @types/react @types/react-native @types/react-navigation @types/react-navigation-stack

echo "Dependencies installed successfully!"
echo "Please restart your development server for the changes to take effect."
