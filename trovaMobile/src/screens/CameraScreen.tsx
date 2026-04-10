// @ts-ignore - Ignore React 19 type issues
import React, { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity, Modal, Platform, ActivityIndicator, Linking } from 'react-native';
import { useRouter } from 'expo-router';
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-react-native';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { detectMonument } from '../services/monumentService';
import SmartGuideChat from '../components/SmartGuideChat';

// Only import VisionCamera on native platforms
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
    console.warn('VisionCamera not available, falling back to ImagePicker');
  }
}

interface MonumentInfo {
  name: string;
  confidence: number;
  description?: string;
  location?: string;
}

const CameraScreen = () => {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [monument, setMonument] = useState<MonumentInfo | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // For native camera
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const cameraRef = useRef<any>(null);
  const devices = Platform.OS !== 'web' && visionCameraAvailable ? useCameraDevices() : null;
  const device = devices?.back;

  // Initialize TensorFlow.js
  const initTF = async () => {
    try {
      // Wait for TensorFlow to be ready
      await tf.ready();
      console.log('TensorFlow.js is ready');

      // Set backend to CPU for better compatibility
      await tf.setBackend('cpu');
      console.log('TensorFlow.js backend set to:', tf.getBackend());
    } catch (error) {
      console.error('Error initializing TensorFlow:', error);
    }
  };

  const pickImage = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permission required', 'Please grant photo library access.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: 'images' as any, // Using string to avoid deprecated MediaTypeOptions
      quality: 0.8,
      base64: false,
    });
    if (!result.canceled && result.assets?.[0]?.uri) {
      setImageUri(result.assets[0].uri);
      await identify(result.assets[0].uri);
    }
  };

  // Request camera permissions for native platforms
  useEffect(() => {
    // Initialize TensorFlow on component mount
    initTF();

    // Request camera permissions for native platforms
    if (Platform.OS !== 'web') {
      (async () => {
        if (visionCameraAvailable) {
          try {
            const cameraPermission = await Camera.requestCameraPermission();
            setHasPermission(cameraPermission === 'granted');
          } catch (error) {
            console.error('Error requesting camera permission:', error);
            setHasPermission(false);
          }
        } else {
          try {
            const perm = await ImagePicker.requestCameraPermissionsAsync();
            setHasPermission(perm.granted);
          } catch (error) {
            console.error('Error requesting camera permission:', error);
            setHasPermission(false);
          }
        }
      })();
    }
  }, []);

  const takePhoto = async () => {
    if (Platform.OS === 'web') {
      // Use ImagePicker on web
      const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
      if (!permissionResult.granted) {
        Alert.alert('Permission required', 'Please grant camera access.');
        return;
      }
      const result = await ImagePicker.launchCameraAsync({
        quality: 0.8,
        base64: false,
      });
      if (!result.canceled && result.assets?.[0]?.uri) {
        setImageUri(result.assets[0].uri);
        await identify(result.assets[0].uri);
      }
    } else {
      // Native: prefer VisionCamera, fallback to ImagePicker
      if (visionCameraAvailable && cameraRef.current && hasPermission) {
        try {
          const photo = await cameraRef.current.takePhoto({
            qualityPrioritization: 'speed',
            flash: 'off',
          });
          const uri = `file://${photo.path}`;
          setImageUri(uri);
          await identify(uri);
        } catch (err) {
          console.error('Error taking photo:', err);
          Alert.alert('Error', 'Failed to take photo. Please try again.');
        }
      } else {
        // Fallback to Expo ImagePicker when VisionCamera is unavailable
        const perm = await ImagePicker.requestCameraPermissionsAsync();
        if (!perm.granted) {
          Alert.alert('Permission required', 'Please grant camera access.');
          return;
        }
        const result = await ImagePicker.launchCameraAsync({
          quality: 0.8,
          base64: false,
        });
        if (!result.canceled && result.assets?.[0]?.uri) {
          setImageUri(result.assets[0].uri);
          await identify(result.assets[0].uri);
        }
      }
    }
  };

  const identify = async (uri: string) => {
    try {
      setLoading(true);

      // Call the monument service
      const result = await detectMonument(uri);

      if (result) {
        setMonument({
          name: result.monumentName,
          confidence: result.confidence,
          description: result.description,
          location: result.location
        });
      }
    } catch (error: any) {
      console.error('Error identifying monument:', error);
      Alert.alert('Error', error?.message || 'Failed to identify monument. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const saveMonument = async () => {
    if (!monument) return;
    try {
      const existing = await AsyncStorage.getItem('favorites');
      const favorites = existing ? JSON.parse(existing) : [];
      const isAlreadySaved = favorites.some((f: any) => f.name === monument.name);

      if (!isAlreadySaved) {
        favorites.push({
          id: Date.now().toString(),
          ...monument,
          date: new Date().toISOString()
        });
        await AsyncStorage.setItem('favorites', JSON.stringify(favorites));
        Alert.alert('Saved', `${monument.name} has been added to your favorites.`);
      } else {
        Alert.alert('Info', 'This monument is already in your favorites.');
      }
    } catch (error) {
      console.error('Error saving favorite:', error);
      Alert.alert('Error', 'Failed to save favorite.');
    }
  };

  const openBooking = () => {
    // Affiliate link logic
    const query = encodeURIComponent(monument?.name || 'Egypt hotels');
    Linking.openURL(`https://www.booking.com/searchresults.html?ss=${query}&aid=123456`);
  };

  // Render different UI based on platform
  const renderCamera = () => {
    if (Platform.OS === 'web') {
      // Web fallback UI
      return (
        <View style={styles.webFallback}>
          <Text style={styles.webNote}>Camera not supported on web preview, please run on Expo Go app.</Text>
          <View style={styles.actionsRow}>
            <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={pickImage}>
              <Ionicons name="images" size={24} color="#fff" />
              <Text style={styles.actionButtonText}>Pick from Gallery</Text>
            </TouchableOpacity>
          </View>
        </View>
      );
    } else if (!visionCameraAvailable) {
      // Native fallback UI when VisionCamera is unavailable
      return (
        <View style={styles.webFallback}>
          <Text style={styles.webNote}>VisionCamera unavailable (Expo Go). Use the fallback below.</Text>
          <View style={styles.actionsRow}>
            <TouchableOpacity style={styles.actionButton} onPress={takePhoto}>
              <Ionicons name="camera" size={24} color="#fff" />
              <Text style={styles.actionButtonText}>Open Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={pickImage}>
              <Ionicons name="images" size={24} color="#fff" />
              <Text style={styles.actionButtonText}>Pick from Gallery</Text>
            </TouchableOpacity>
          </View>
        </View>
      );
    } else if (!device || hasPermission === null) {
      // Loading state
      return <Text style={styles.info}>Loading camera...</Text>;
    } else if (hasPermission === false) {
      // Permission denied
      return <Text style={styles.info}>No access to camera</Text>;
    } else {
      // Native camera UI
      return (
        <View style={styles.cameraContainer}>
          <Camera
            ref={cameraRef}
            style={styles.camera}
            device={device}
            isActive={true}
            photo={true}
          />
          <TouchableOpacity style={styles.captureButton} onPress={takePhoto}>
            <Ionicons name="camera" size={32} color="#fff" />
          </TouchableOpacity>
        </View>
      );
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color="#1666c1" />
        <Text style={styles.loadingText}>Identifying monument...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Discover Egypt AI</Text>
      <Text style={styles.subtitle}>Capture or select a photo to identify monuments</Text>

      {!imageUri ? (
        // Show camera or fallback UI when no image is captured
        renderCamera()
      ) : (
        // Show actions row when image is captured
        <View style={styles.actionsRow}>
          <TouchableOpacity style={styles.actionButton} onPress={takePhoto}>
            <Ionicons name="camera" size={24} color="#fff" />
            <Text style={styles.actionButtonText}>Open Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={pickImage}>
            <Ionicons name="images" size={24} color="#fff" />
            <Text style={styles.actionButtonText}>Pick from Gallery</Text>
          </TouchableOpacity>
        </View>
      )}

      {imageUri && (
        <Image source={{ uri: imageUri }} style={styles.preview} />
      )}

      {loading && <Text style={styles.info}>Identifying monument...</Text>}

      {monument && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>{monument.name || 'Unknown Monument'}</Text>
          <Text style={styles.resultSubtitle}>Confidence: {(monument.confidence * 100).toFixed(1)}%</Text>

          <TouchableOpacity style={styles.askButton} onPress={() => setChatOpen(true)}>
            <Ionicons name="chatbubble-ellipses" size={20} color="#fff" />
            <Text style={styles.askButtonText}>Ask About This</Text>
          </TouchableOpacity>

          <View style={styles.actionButtonsContainer}>
            <TouchableOpacity
              style={[styles.actionButton, styles.saveButton]}
              onPress={saveMonument}
            >
              <Ionicons name="heart" size={20} color="#fff" />
              <Text style={styles.actionButtonText}>Save</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.actionButton, styles.planButton]}
              onPress={() => {
                router.push({
                  pathname: '/plan-itinerary',
                  params: { destination: monument.location || 'Egypt', interest: monument.name }
                });
              }}
            >
              <Ionicons name="map" size={20} color="#fff" />
              <Text style={styles.actionButtonText}>Plan Visit</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.actionButton, styles.bookButton]}
            onPress={openBooking}
          >
            <Ionicons name="ticket" size={20} color="#fff" />
            <Text style={styles.actionButtonText}>Book Tickets / Tours</Text>
          </TouchableOpacity>
        </View>
      )}

      <Modal visible={chatOpen} animationType="slide" onRequestClose={() => setChatOpen(false)}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Ask About {monument?.name || 'the Monument'}</Text>
          <TouchableOpacity onPress={() => setChatOpen(false)}>
            <Ionicons name="close-circle" size={28} color="#333" />
          </TouchableOpacity>
        </View>
        <View style={{ flex: 1 }}>
          <SmartGuideChat initialLocation={monument?.name || undefined} />
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#f5f7fb' },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    color: '#555',
    fontSize: 16,
  },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 6, color: '#333' },
  subtitle: { fontSize: 14, color: '#666', marginBottom: 12 },
  actionsRow: { flexDirection: 'row', gap: 10, marginBottom: 12 },
  actionButton: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#1666c1', paddingVertical: 10, paddingHorizontal: 12, borderRadius: 10 },
  secondaryButton: { backgroundColor: '#4f8bc9' },
  actionButtonText: { color: '#fff', fontWeight: '600' },
  preview: { width: '100%', height: 240, borderRadius: 12, marginBottom: 12, resizeMode: 'cover' },
  info: { color: '#333', marginBottom: 8 },
  resultCard: { backgroundColor: '#fff', borderRadius: 12, padding: 12, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 6, elevation: 2 },
  resultTitle: { fontSize: 18, fontWeight: '700' },
  resultSubtitle: { fontSize: 13, color: '#666', marginTop: 4 },
  askButton: { marginTop: 12, backgroundColor: '#2f7b2d', flexDirection: 'row', alignItems: 'center', gap: 8, paddingVertical: 10, paddingHorizontal: 12, borderRadius: 8, alignSelf: 'flex-start' },
  askButtonText: { color: '#fff', fontWeight: '600' },
  modalHeader: { padding: 12, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#eee' },
  modalTitle: { fontSize: 18, fontWeight: '600' },
  // Camera styles
  cameraContainer: { width: '100%', height: 300, borderRadius: 10, overflow: 'hidden', position: 'relative', marginBottom: 20 },
  camera: { flex: 1 },
  captureButton: { position: 'absolute', bottom: 20, alignSelf: 'center', backgroundColor: 'rgba(0,0,0,0.5)', borderRadius: 30, padding: 15 },
  webFallback: { width: '100%', height: 200, backgroundColor: '#e0e0e0', borderRadius: 10, justifyContent: 'center', alignItems: 'center', padding: 20, marginBottom: 20 },
  webNote: { fontSize: 16, color: '#666', textAlign: 'center', marginBottom: 20 },
  actionButtonsContainer: { flexDirection: 'row', gap: 10, marginTop: 12 },
  saveButton: { backgroundColor: '#E91E63', flex: 1, justifyContent: 'center' },
  planButton: { backgroundColor: '#FF9800', flex: 1, justifyContent: 'center' },
  bookButton: { backgroundColor: '#003580', marginTop: 10, justifyContent: 'center', width: '100%' },
});

export default CameraScreen;
