import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
// VisionCamera is only available on native; dynamically require to avoid web bundling issues
let Camera: any;
let useCameraDevices: any;
let visionCameraAvailable = false;
if (Platform.OS !== 'web') {
  try {
    const VisionCamera = require('react-native-vision-camera');
    Camera = VisionCamera.Camera;
    useCameraDevices = VisionCamera.useCameraDevices;
    visionCameraAvailable = true;
  } catch (e) {
    console.warn('VisionCamera not available, will use ImagePicker fallback');
  }
}
import { identifyMonument } from '@/src/api/visionService';
import * as tf from '@tensorflow/tfjs';
// bundleResourceIO removed for web compatibility
// import { bundleResourceIO } from '@tensorflow/tfjs-react-native';
import { router } from 'expo-router';

interface MonumentInfo {
  name: string;
  description: string;
  confidence: number;
}

const ARGuideScreen: React.FC = () => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [monumentInfo, setMonumentInfo] = useState<MonumentInfo | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const cameraRef = useRef<any>(null);
  const devices = Platform.OS !== 'web' && visionCameraAvailable ? useCameraDevices?.() : null;
  const device = devices?.back;

  // Request camera permissions
  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        if (visionCameraAvailable) {
          const cameraPermission = await Camera.requestCameraPermission();
          setHasPermission(cameraPermission === 'granted');
        } else {
          const perm = await (await import('expo-image-picker')).requestCameraPermissionsAsync();
          setHasPermission(perm.granted);
        }
        try {
          await import('@tensorflow/tfjs-react-native');
        } catch (e) {
          console.warn('tfjs-react-native not available on this platform', e);
        }
        await tf.ready();
        console.log('TensorFlow.js is ready');
      } else {
        // Web does not support VisionCamera; set permission to false and show fallback UI
        setHasPermission(false);
      }
    })();
  }, []);

  // Function to capture frame and send to backend
  const captureAndIdentify = async () => {
    if (Platform.OS === 'web') {
      Alert.alert('Not supported on web', 'AR camera capture is only available on mobile (Expo Go).');
      return;
    }
    if (isProcessing) return;
    try {
      setIsProcessing(true);
      if (visionCameraAvailable && cameraRef.current) {
        const photo = await cameraRef.current.takePhoto({
          qualityPrioritization: 'speed',
          flash: 'off',
        });
        const uri = `file://${photo.path}`;
        const response = await identifyMonument(uri);
        if (response && response.identified_monument) {
          setMonumentInfo({
            name: response.identified_monument,
            description: 'No description available',
            confidence: response.confidence || 0,
          });
        }
      } else {
        const ImagePicker = await import('expo-image-picker');
        const perm = await ImagePicker.requestCameraPermissionsAsync();
        if (!perm.granted) {
          Alert.alert('Permission required', 'Please grant camera access.');
          return;
        }
        const result = await ImagePicker.launchCameraAsync({ quality: 0.8, base64: false });
        if (!result.canceled && result.assets?.[0]?.uri) {
          const response = await identifyMonument(result.assets[0].uri);
          if (response && response.identified_monument) {
            setMonumentInfo({
              name: response.identified_monument,
              description: 'No description available',
              confidence: response.confidence || 0,
            });
          }
        }
      }
    } catch (error) {
      console.error('Error identifying monument:', error);
      Alert.alert('Error', 'Failed to identify monument. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Function to ask more details about the monument
  const askMoreDetails = async () => {
    if (!monumentInfo) return;
    
    // Navigate to SmartGuideChat screen with the monument name as a parameter
    router.push({
      pathname: '/smart-guide-chat',
      params: { location: monumentInfo.name }
    });
  };

  if (hasPermission === null) {
    return <View style={styles.container}><Text>Requesting camera permission...</Text></View>;
  }

  if (hasPermission === false) {
    if (Platform.OS === 'web') {
      return (
        <View style={styles.container}>
          <View style={styles.webFallback}>
            <Text style={styles.webNote}>AR Guide camera is not supported on web. Please run on Expo Go (Android/iOS).</Text>
          </View>
        </View>
      );
    }
    return <View style={styles.container}><Text>No access to camera</Text></View>;
  }

  if (!device) {
    return <View style={styles.container}><Text>Loading camera...</Text></View>;
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={styles.camera}
        device={device}
        isActive={true}
        photo={true}
      />
      
      {/* AR Overlay with monument info */}
      {monumentInfo && (
        <View style={styles.overlay}>
          <View style={styles.infoCard}>
            <Text style={styles.monumentName}>{monumentInfo.name}</Text>
            <Text style={styles.monumentDescription}>
              {monumentInfo.description}
            </Text>
            <Text style={styles.confidenceText}>
              Confidence: {(monumentInfo.confidence * 100).toFixed(1)}%
            </Text>
          </View>
        </View>
      )}
      
      {/* Control buttons */}
      <View style={styles.controls}>
        <TouchableOpacity 
          style={styles.captureButton} 
          onPress={captureAndIdentify}
          disabled={isProcessing}
        >
          <Text style={styles.buttonText}>
            {isProcessing ? 'Processing...' : 'Identify'}
          </Text>
        </TouchableOpacity>
        
        {monumentInfo && (
          <TouchableOpacity 
            style={styles.askButton} 
            onPress={askMoreDetails}
          >
            <Text style={styles.buttonText}>Chat with Guide</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  infoCard: {
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    borderRadius: 10,
    padding: 20,
    margin: 20,
    maxWidth: '80%',
  },
  monumentName: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  monumentDescription: {
    color: 'white',
    fontSize: 16,
    marginBottom: 10,
  },
  confidenceText: {
    color: '#aaa',
    fontSize: 14,
  },
  controls: {
    position: 'absolute',
    bottom: 30,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  captureButton: {
    backgroundColor: '#2196F3',
    padding: 15,
    borderRadius: 50,
    marginHorizontal: 10,
  },
  askButton: {
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 50,
    marginHorizontal: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  // Web fallback styles
  webFallback: { width: '100%', height: 200, backgroundColor: '#222', borderRadius: 10, justifyContent: 'center', alignItems: 'center', padding: 20 },
  webNote: { fontSize: 16, color: '#ddd', textAlign: 'center' },
});

export default ARGuideScreen;