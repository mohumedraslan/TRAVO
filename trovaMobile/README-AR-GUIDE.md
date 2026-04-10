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
  
## Installation notes for TensorFlow on Expo SDK 54

- If you encounter peer dependency conflicts when installing `@tensorflow/tfjs-react-native` with Expo SDK 54 (for example conflicts with `expo-camera`), you can force install using the following helper script from the project root:

```powershell
npm run install:legacy
```

- That runs `npm install --legacy-peer-deps` and will allow the TF packages to be installed despite peer dependency warnings. Use this only if you understand the risk of ignoring peer dependency constraints.

- If you'd prefer a longer-term solution (or if `@tensorflow/tfjs-react-native` is not working on your Expo/React Native version), consider switching to `onnxruntime-react-native` for on-device inference. ONNX Runtime has active native support for mobile and can run converted ONNX models with good performance. Migration notes:
	- Convert your model to ONNX format (from PyTorch/TensorFlow). Use the official converters.
	- Add `onnxruntime-react-native` and follow the native install steps in its README (it requires native linking / config on Android/iOS).
	- Replace TFJS model load/predict calls with ONNX runtime session run calls. ONNX runtime tends to have fewer Expo peer-dependency issues since it focuses on native bindings.

Recommended quick checklist after install:
- Verify `expo-gl` and `expo-gl-cpp` are installed (they're required for tfjs-react-native). They are already included in this project dependencies.
- For on-device TFJS: ensure you initialize TF before inference by dynamically importing `@tensorflow/tfjs-react-native` and awaiting `tf.ready()` (see `src/screens/ARGuideScreen.tsx` and `src/screens/CameraScreen.tsx`).
- Rebuild the app on device (Expo Go may not support native modules — use `expo run:android` / `expo run:ios` or a dev client).

Android emulator tip

- When testing from an Android emulator, local backend requests to `localhost` or `127.0.0.1` must instead use `10.0.2.2`. For example set:

```powershell
# from the mobile app folder
setx NEXT_PUBLIC_BACKEND_BASE "http://10.0.2.2:8000/api"
```

Or set the env var in your shell before starting the web/dev server. The mobile `axios` client also swaps `127.0.0.1` to `10.0.2.2` on Android, but web demos (Next.js) should use NEXT_PUBLIC_BACKEND_BASE when testing on emulator.
- Implement caching for monument information
- Add offline support for basic functionality
- Enhance AR overlay with 3D models and animations
- Improve voice recognition accuracy