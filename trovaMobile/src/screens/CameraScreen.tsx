import React from 'react';
import { View, Text, Button, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

const CameraScreen: React.FC<any> = () => {
  const recognizeObjectPlaceholder = async () => {
    try {
      // Placeholder: this would send an image to vision_service in backend
      const res = await axios.post('http://localhost:8000/api/vision/recognize', {
        image: 'data:image/png;base64,<placeholder>'
      });
      Alert.alert('Recognition result', JSON.stringify(res.data));
    } catch (err: any) {
      Alert.alert('Recognition failed', err?.response?.data?.message || 'Service not available yet');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Camera</Text>
      <Text style={styles.subtitle}>Object recognition placeholder</Text>
      <Button title="Run recognition" onPress={recognizeObjectPlaceholder} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#555', marginBottom: 16 },
});

export default CameraScreen;
