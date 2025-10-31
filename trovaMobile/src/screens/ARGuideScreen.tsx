import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { identifyMonument } from '@/src/api/visionService';
import * as tf from '@tensorflow/tfjs';
import { bundleResourceIO } from '@tensorflow/tfjs-react-native';
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
  const cameraRef = useRef<Camera>(null);
  const devices = useCameraDevices();
  const device = devices.back;

  // Request camera permissions
  useEffect(() => {
    (async () => {
      const cameraPermission = await Camera.requestCameraPermission();
      setHasPermission(cameraPermission === 'granted');
      
      // Initialize TensorFlow.js
      await tf.ready();
      console.log('TensorFlow.js is ready');
    })();
  }, []);

  // Function to capture frame and send to backend
  const captureAndIdentify = async () => {
    if (cameraRef.current && !isProcessing) {
      try {
        setIsProcessing(true);
        
        // Capture photo
        const photo = await cameraRef.current.takePhoto({
          qualityPrioritization: 'speed',
          flash: 'off',
        });
        
        // Create form data for API request
        const formData = new FormData();
        formData.append('file', {
          uri: `file://${photo.path}`,
          type: 'image/jpeg',
          name: 'monument.jpg',
        } as any);
        
        // Send to backend
        const response = await identifyMonument(`file://${photo.path}`);
        
        // Update state with monument info
        if (response && response.identified_monument) {
          setMonumentInfo({
            name: response.identified_monument,
            description: response.description || 'No description available',
            confidence: response.confidence || 0,
          });
        }
      } catch (error) {
        console.error('Error identifying monument:', error);
        Alert.alert('Error', 'Failed to identify monument. Please try again.');
      } finally {
        setIsProcessing(false);
      }
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
});

export default ARGuideScreen;