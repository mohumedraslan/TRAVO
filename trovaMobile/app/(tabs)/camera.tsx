import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, Image, ActivityIndicator, TouchableOpacity, ScrollView } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';
import client from '../../src/api/client';

interface IdentificationResult {
  identified_monument: string;
  confidence: number;
  description?: string;
  fun_fact?: string;
  location?: string;
}

interface PhotoMeta {
  photoId?: string;
  storageUrl?: string;
  saved: boolean;
}

export default function CameraTab() {
  const [image, setImage] = useState<string | null>(null);
  const [imageBlob, setImageBlob] = useState<Blob | null>(null);
  const [result, setResult] = useState<IdentificationResult | null>(null);
  const [photoMeta, setPhotoMeta] = useState<PhotoMeta | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [gpsLocation, setGpsLocation] = useState<{ lat: number, lon: number } | null>(null);

  const getLocation = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === 'granted') {
        const loc = await Location.getCurrentPositionAsync({});
        setGpsLocation({ lat: loc.coords.latitude, lon: loc.coords.longitude });
      }
    } catch { }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Please allow access to your photos.');
      return;
    }

    const pickerResult = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      quality: 0.8,
    });

    if (!pickerResult.canceled && pickerResult.assets[0]) {
      const asset = pickerResult.assets[0];
      setImage(asset.uri);
      setResult(null);
      setPhotoMeta(null);
      await getLocation();
      await identifyImage(asset);
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Please allow camera access.');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      const asset = result.assets[0];
      setImage(asset.uri);
      setResult(null);
      setPhotoMeta(null);
      await getLocation();
      await identifyImage(asset);
    }
  };

  const identifyImage = async (asset: ImagePicker.ImagePickerAsset) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: asset.uri,
        type: 'image/jpeg',
        name: 'photo.jpg',
      } as any);

      const response = await client.post('/vision/identify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      });

      setResult(response.data);
    } catch (err: any) {
      console.error('Identification error:', err);
      setResult({
        identified_monument: 'Unknown Location',
        confidence: 0.3,
        description: 'Could not connect to server. Check network settings.',
      });
    } finally {
      setLoading(false);
    }
  };

  const savePhoto = async () => {
    if (!image || !result) return;
    setSaving(true);

    try {
      // Upload to storage
      const formData = new FormData();
      formData.append('image', {
        uri: image,
        type: 'image/jpeg',
        name: 'photo.jpg',
      } as any);
      formData.append('user_id', 'demo_user');

      const uploadRes = await client.post('/storage/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000,
      });

      setPhotoMeta({
        photoId: uploadRes.data.photo_id,
        storageUrl: uploadRes.data.public_url,
        saved: true,
      });

      Alert.alert('✅ Photo Saved!', `"${result.identified_monument}" added to your timeline.`);
    } catch (err) {
      console.error('Save error:', err);
      Alert.alert('Save Failed', 'Could not save photo. Try again.');
    } finally {
      setSaving(false);
    }
  };

  const deepScan = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: image,
        type: 'image/jpeg',
        name: 'photo.jpg',
      } as any);

      const response = await client.post('/vision/deep_scan', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      });

      setResult(response.data);
    } catch (err: any) {
      Alert.alert('Deep Scan Error', 'Cloud AI service unavailable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📷 Capture</Text>
      <Text style={styles.subtitle}>Take or select a photo for AI identification</Text>

      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.captureButton} onPress={takePhoto}>
          <Text style={styles.captureButtonText}>📸 Take Photo</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.galleryButton} onPress={pickImage}>
          <Text style={styles.galleryButtonText}>🖼️ Gallery</Text>
        </TouchableOpacity>
      </View>

      {image && (
        <View style={styles.imageContainer}>
          <Image source={{ uri: image }} style={styles.image} />
          {gpsLocation && (
            <Text style={styles.gpsText}>📍 {gpsLocation.lat.toFixed(4)}, {gpsLocation.lon.toFixed(4)}</Text>
          )}
        </View>
      )}

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Analyzing with AI...</Text>
        </View>
      )}

      {result && !loading && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>{result.identified_monument}</Text>
          <Text style={styles.confidence}>
            {result.confidence >= 0.7 ? '✅' : '⚠️'} Confidence: {(result.confidence * 100).toFixed(0)}%
          </Text>
          {result.location && <Text style={styles.location}>📍 {result.location}</Text>}
          {result.description && <Text style={styles.description}>{result.description}</Text>}
          {result.fun_fact && <Text style={styles.funFact}>💡 {result.fun_fact}</Text>}

          <View style={styles.actionButtons}>
            {result.confidence < 0.6 && (
              <TouchableOpacity style={styles.deepScanButton} onPress={deepScan}>
                <Text style={styles.deepScanButtonText}>🔍 Deep Scan</Text>
              </TouchableOpacity>
            )}

            {!photoMeta?.saved ? (
              <TouchableOpacity
                style={[styles.saveButton, saving && styles.savingButton]}
                onPress={savePhoto}
                disabled={saving}
              >
                <Text style={styles.saveButtonText}>
                  {saving ? '⏳ Saving...' : '💾 Save to Timeline'}
                </Text>
              </TouchableOpacity>
            ) : (
              <View style={styles.savedBadge}>
                <Text style={styles.savedText}>✅ Saved to Timeline</Text>
              </View>
            )}
          </View>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  title: { fontSize: 28, fontWeight: 'bold', marginTop: 40 },
  subtitle: { fontSize: 14, color: '#666', marginBottom: 20 },
  buttonRow: { flexDirection: 'row', gap: 12 },
  captureButton: { flex: 1, backgroundColor: '#007AFF', borderRadius: 12, padding: 16, alignItems: 'center' },
  captureButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  galleryButton: { flex: 1, backgroundColor: '#f0f0f0', borderRadius: 12, padding: 16, alignItems: 'center' },
  galleryButtonText: { color: '#333', fontSize: 16, fontWeight: '600' },
  imageContainer: { marginTop: 20, alignItems: 'center' },
  image: { width: 300, height: 300, borderRadius: 16 },
  gpsText: { fontSize: 12, color: '#666', marginTop: 8 },
  loadingContainer: { marginTop: 30, alignItems: 'center' },
  loadingText: { marginTop: 10, color: '#666' },
  resultContainer: { marginTop: 20, padding: 16, backgroundColor: '#f9f9f9', borderRadius: 12 },
  resultTitle: { fontSize: 22, fontWeight: 'bold' },
  confidence: { fontSize: 14, color: '#666', marginTop: 4 },
  location: { fontSize: 14, color: '#1976d2', marginTop: 4 },
  description: { fontSize: 14, marginTop: 10, lineHeight: 20 },
  funFact: { fontSize: 14, fontStyle: 'italic', color: '#007AFF', marginTop: 10 },
  actionButtons: { marginTop: 16, gap: 10 },
  deepScanButton: { backgroundColor: '#6200ea', borderRadius: 10, padding: 14, alignItems: 'center' },
  deepScanButtonText: { color: '#fff', fontWeight: '600', fontSize: 15 },
  saveButton: { backgroundColor: '#4caf50', borderRadius: 10, padding: 14, alignItems: 'center' },
  savingButton: { backgroundColor: '#9e9e9e' },
  saveButtonText: { color: '#fff', fontWeight: '600', fontSize: 15 },
  savedBadge: { backgroundColor: '#e8f5e9', borderRadius: 10, padding: 14, alignItems: 'center' },
  savedText: { color: '#2e7d32', fontWeight: '600' },
});
