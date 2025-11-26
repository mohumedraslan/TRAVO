import React, { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity, Platform, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import { supabase } from '../config/supabase';
import { api } from '../api/client';

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

const CameraScreen = () => {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const router = useRouter();

  // For native camera
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const cameraRef = useRef<any>(null);
  const devices = Platform.OS !== 'web' && visionCameraAvailable ? useCameraDevices() : null;
  const device = devices?.back;

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web' && visionCameraAvailable) {
        const status = await Camera.requestCameraPermission();
        setHasPermission(status === 'granted');
      } else {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        setHasPermission(status === 'granted');
      }
    })();
  }, []);

  const takePhoto = async () => {
    try {
      if (Platform.OS === 'web' || !visionCameraAvailable) {
        const result = await ImagePicker.launchCameraAsync({
          quality: 0.5,
          base64: true,
        });
        if (!result.canceled && result.assets[0]) {
          setImageUri(result.assets[0].uri);
          processPhoto(result.assets[0]);
        }
      } else if (cameraRef.current) {
        const photo = await cameraRef.current.takePhoto({
          qualityPrioritization: 'speed',
          flash: 'off',
        });
        const uri = `file://${photo.path}`;
        setImageUri(uri);
        // For native, we need to read base64 if not provided, or upload file directly
        // VisionCamera doesn't return base64 by default.
        // For MVP, let's use ImagePicker on native too if VisionCamera is complex to get base64 quickly without FS
        // Or just use ImagePicker for consistency and ease.
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to take photo');
    }
  };

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: 'images',
      quality: 0.5,
      base64: true,
    });
    if (!result.canceled && result.assets[0]) {
      setImageUri(result.assets[0].uri);
      processPhoto(result.assets[0]);
    }
  };

  const processPhoto = async (asset: ImagePicker.ImagePickerAsset) => {
    setLoading(true);
    setResult(null);

    try {
      // 1. Get Active Trip
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        Alert.alert('Login Required', 'Please log in to save to your diary.');
        setLoading(false);
        return;
      }

      const { data: trip } = await supabase
        .from('trips')
        .select('id')
        .eq('user_id', user.id)
        .eq('status', 'active')
        .single();

      if (!trip) {
        Alert.alert('No Active Trip', 'Please start a trip from the Home screen first.');
        setLoading(false);
        return;
      }

      // 2. GPS (Default to 0,0 if not available)
      // TODO: Install expo-location for real GPS
      const gpsLat = 0.0;
      const gpsLon = 0.0;

      // 3. Send to Backend (Diary Service)
      // We need to send FormData
      const formData = new FormData();
      formData.append('trip_id', trip.id);
      formData.append('gps_lat', String(gpsLat));
      formData.append('gps_lon', String(gpsLon));

      // Append file
      const filename = asset.uri.split('/').pop() || 'photo.jpg';
      const match = /\.(\w+)$/.exec(filename);
      const type = match ? `image/${match[1]}` : `image`;

      formData.append('file', {
        uri: asset.uri,
        name: filename,
        type: type,
      } as any);

      // Get session token for backend auth
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      // Call API
      const response = await api.post('/diary/identify', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': token ? `Bearer ${token}` : '',
        },
      });

      setResult(response.data);
      Alert.alert('Success', `Logged: ${response.data.place_name}`);

    } catch (error: any) {
      console.error('Error processing photo:', error);
      Alert.alert('Error', 'Failed to process photo. ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Capture Moment</Text>

      {imageUri ? (
        <View style={styles.previewContainer}>
          <Image source={{ uri: imageUri }} style={styles.preview} />
          {loading && (
            <View style={styles.loadingOverlay}>
              <ActivityIndicator size="large" color="#fff" />
              <Text style={styles.loadingText}>Identifying & Logging...</Text>
            </View>
          )}
          {result && (
            <View style={styles.resultOverlay}>
              <Ionicons name="checkmark-circle" size={48} color="#4CAF50" />
              <Text style={styles.resultText}>{result.place_name}</Text>
            </View>
          )}
        </View>
      ) : (
        <View style={styles.placeholder}>
          <Ionicons name="camera-outline" size={64} color="#ccc" />
          <Text style={styles.placeholderText}>Take a photo to log it to your diary</Text>
        </View>
      )}

      <View style={styles.controls}>
        <TouchableOpacity style={styles.button} onPress={takePhoto}>
          <Ionicons name="camera" size={24} color="#fff" />
          <Text style={styles.buttonText}>Camera</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.secondaryButton]} onPress={pickImage}>
          <Ionicons name="images" size={24} color="#fff" />
          <Text style={styles.buttonText}>Gallery</Text>
        </TouchableOpacity>
      </View>

      {result && (
        <TouchableOpacity style={styles.viewDiaryButton} onPress={() => router.push('/(tabs)/diary')}>
          <Text style={styles.viewDiaryText}>View in Diary</Text>
          <Ionicons name="arrow-forward" size={20} color="#fff" />
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, marginTop: 40 },
  previewContainer: { width: '100%', height: 400, borderRadius: 20, overflow: 'hidden', marginBottom: 20, position: 'relative' },
  preview: { width: '100%', height: '100%' },
  placeholder: { width: '100%', height: 400, backgroundColor: '#f5f5f5', borderRadius: 20, justifyContent: 'center', alignItems: 'center', marginBottom: 20 },
  placeholderText: { color: '#999', marginTop: 10 },
  controls: { flexDirection: 'row', gap: 20, width: '100%' },
  button: { flex: 1, backgroundColor: '#000', padding: 15, borderRadius: 12, alignItems: 'center', flexDirection: 'row', justifyContent: 'center', gap: 8 },
  secondaryButton: { backgroundColor: '#666' },
  buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  loadingOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: '#fff', marginTop: 10, fontWeight: 'bold' },
  resultOverlay: { position: 'absolute', bottom: 0, left: 0, right: 0, backgroundColor: 'rgba(255,255,255,0.9)', padding: 20, alignItems: 'center' },
  resultText: { fontSize: 18, fontWeight: 'bold', color: '#333', marginTop: 5 },
  viewDiaryButton: { marginTop: 20, backgroundColor: '#4CAF50', paddingHorizontal: 30, paddingVertical: 12, borderRadius: 25, flexDirection: 'row', alignItems: 'center', gap: 5 },
  viewDiaryText: { color: '#fff', fontWeight: 'bold' },
});

export default CameraScreen;
