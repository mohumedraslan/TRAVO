# TRAVO Mobile App - AR Guide and Smart Chat Components

## Overview

This document provides information about the newly implemented AR Guide Screen and Smart Guide Chat components for the TRAVO mobile application.

## Components

### 1. AR Guide Screen

The AR Guide Screen provides an augmented reality experience for identifying monuments and landmarks using the device camera.

**Features:**
- Live camera feed with real-time monument recognition
- Overlay display of monument information
- Integration with TensorFlow.js for on-device inference
- Direct access to the Smart Guide Chat for more detailed information

**Files:**
- `src/screens/ARGuideScreen.tsx` - Main AR screen component
- `app/(tabs)/ar-guide.tsx` - Tab navigation integration
- `src/api/visionService.ts` - API service for monument identification

**Usage:**
1. Navigate to the AR Guide tab in the app
2. Point the camera at a monument or landmark
3. Tap the "Identify" button to recognize the monument
4. View the overlay with monument information
5. Tap "Chat with Guide" to get more detailed information

### 2. Smart Guide Chat

The Smart Guide Chat component provides a conversational interface to interact with the TRAVO assistant service.

**Features:**
- Text and voice input options
- Conversational history display
- Voice-to-text and text-to-voice capabilities
- Real-time communication using socket.io

**Files:**
- `src/components/SmartGuideChat.tsx` - Main chat component
- `src/screens/SmartGuideChatScreen.tsx` - Standalone screen wrapper
- `app/smart-guide-chat.tsx` - Modal route for the chat screen
- `src/api/assistantService.ts` - API service for assistant interactions

**Usage:**
1. Access the chat from the AR Guide screen or directly from the app
2. Type messages or use the microphone button for voice input
3. Receive text and audio responses from the assistant

## API Integration

These components integrate with the following backend endpoints:

- `/api/vision/identify` - For monument identification from images
- `/api/assistant/ask` - For text-based queries to the assistant
- `/api/assistant/voice_to_text` - For converting voice recordings to text
- `/api/assistant/text_to_voice` - For converting text responses to speech

## Dependencies

The implementation uses the following key dependencies:

- `react-native-vision-camera` - For camera access and photo capture
- `@tensorflow/tfjs` and `@tensorflow/tfjs-react-native` - For on-device inference
- `expo-camera`, `expo-gl`, `expo-gl-cpp` - For camera and graphics support
- `react-native-fs` - For file system operations
- `axios` - For API requests
- `socket.io-client` - For real-time communication
- `expo-av` - For audio recording and playback

## Future Improvements

- Replace the TensorFlow.js placeholder with a real on-device model
- Implement caching for monument information
- Add offline support for basic functionality
- Enhance AR overlay with 3D models and animations
- Improve voice recognition accuracy