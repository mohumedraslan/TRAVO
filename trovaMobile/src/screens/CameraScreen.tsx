import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Alert, Image, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';
import client from '../api/client';

interface IdentificationResult {
  identified_monument: string;
  confidence: number;
  description?: string;
  fun_fact?: string;
}

const CameraScreen: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [result, setResult] = useState<IdentificationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const pickImage = async () => {
    // Request permissions
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Please allow access to your photos.');
      return;
    }

    const pickerResult = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      quality: 0.8,
      base64: true,
    });

    if (!pickerResult.canceled && pickerResult.assets[0]) {
      const asset = pickerResult.assets[0];
      setImage(asset.uri);
      setResult(null);
      await identifyImage(asset);
    }
  };

  const identifyImage = async (asset: ImagePicker.ImagePickerAsset) => {
    setLoading(true);
    try {
      // Get location (optional)
      let locationData = null;
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status === 'granted') {
          const loc = await Location.getCurrentPositionAsync({});
          locationData = { lat: loc.coords.latitude, lon: loc.coords.longitude };
        }
      } catch { }

      // Create form data for upload
      const formData = new FormData();
      formData.append('image', {
        uri: asset.uri,
        type: 'image/jpeg',
        name: 'photo.jpg',
      } as any);

      const response = await client.post('/vision/identify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000,
      });

      setResult(response.data);
    } catch (err: any) {
      console.error('Identification error:', err);
      Alert.alert('Error', err?.response?.data?.detail || 'Failed to identify. Check network.');
    } finally {
      setLoading(false);
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
      Alert.alert('Deep Scan Error', err?.response?.data?.detail || 'Cloud AI failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📸 AI Photo Identifier</Text>
      <Text style={styles.subtitle}>Select a photo to identify monuments</Text>

      <Button title="Pick an Image" onPress={pickImage} />

      {image && (
        <View style={styles.imageContainer}>
          <Image source={{ uri: image }} style={styles.image} />
        </View>
      )}

      {loading && <ActivityIndicator size="large" color="#007AFF" style={{ marginTop: 20 }} />}

      {result && !loading && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>{result.identified_monument}</Text>
          <Text style={styles.confidence}>Confidence: {(result.confidence * 100).toFixed(1)}%</Text>
          {result.description && <Text style={styles.description}>{result.description}</Text>}
          {result.fun_fact && <Text style={styles.funFact}>💡 {result.fun_fact}</Text>}

          {result.confidence < 0.6 && (
            <Button title="🔍 Deep Scan (Cloud AI)" onPress={deepScan} />
          )}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#666', marginBottom: 16 },
  imageContainer: { marginTop: 16, alignItems: 'center' },
  image: { width: 300, height: 300, borderRadius: 12 },
  resultContainer: { marginTop: 20, padding: 16, backgroundColor: '#f5f5f5', borderRadius: 12 },
  resultTitle: { fontSize: 20, fontWeight: '600' },
  confidence: { fontSize: 14, color: '#666', marginTop: 4 },
  description: { fontSize: 14, marginTop: 8 },
  funFact: { fontSize: 14, fontStyle: 'italic', color: '#007AFF', marginTop: 8 },
});

export default CameraScreen;
