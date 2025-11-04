import React, { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity, Modal, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { identifyMonument } from '@/src/api/visionService';
import SmartGuideChat from '@/src/components/SmartGuideChat';
import { IconSymbol } from '@/components/ui/icon-symbol';

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
}

const CameraScreen: React.FC<any> = () => {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [monument, setMonument] = useState<MonumentInfo | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // For native camera
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const cameraRef = useRef<any>(null);
  const devices = Platform.OS !== 'web' && visionCameraAvailable ? useCameraDevices() : null;
  const device = devices?.back;

  const pickImage = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permission required', 'Please grant photo library access.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
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
    if (Platform.OS !== 'web') {
      (async () => {
        if (visionCameraAvailable) {
          const cameraPermission = await Camera.requestCameraPermission();
          setHasPermission(cameraPermission === 'granted');
        } else {
          const perm = await ImagePicker.requestCameraPermissionsAsync();
          setHasPermission(perm.granted);
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
      const res = await identifyMonument(uri);
      setMonument({ name: res.identified_monument, confidence: res.confidence });
    } catch (err: any) {
      console.error(err);
      Alert.alert('Identification failed', err?.response?.data?.detail || 'Please try again.');
    } finally {
      setLoading(false);
    }
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
              <IconSymbol name="photo.fill" size={24} color="#fff" />
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
              <IconSymbol name="camera.fill" size={24} color="#fff" />
              <Text style={styles.actionButtonText}>Open Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={pickImage}>
              <IconSymbol name="photo.fill" size={24} color="#fff" />
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
            <IconSymbol name="camera.fill" size={32} color="#fff" />
          </TouchableOpacity>
        </View>
      );
    }
  };

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
            <IconSymbol name="camera.fill" size={24} color="#fff" />
            <Text style={styles.actionButtonText}>Open Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={pickImage}>
            <IconSymbol name="photo.fill" size={24} color="#fff" />
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
            <IconSymbol name="text.bubble.fill" size={20} color="#fff" />
            <Text style={styles.askButtonText}>Ask About This</Text>
          </TouchableOpacity>
        </View>
      )}

      <Modal visible={chatOpen} animationType="slide" onRequestClose={() => setChatOpen(false)}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Ask About {monument?.name || 'the Monument'}</Text>
          <TouchableOpacity onPress={() => setChatOpen(false)}>
            <IconSymbol name="xmark.circle.fill" size={28} color="#333" />
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
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 6 },
  subtitle: { fontSize: 14, color: '#555', marginBottom: 12 },
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
});

export default CameraScreen;
