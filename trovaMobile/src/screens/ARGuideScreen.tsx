import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const ARGuideScreen: React.FC = () => {
  return (
    <View style={styles.comingSoonContainer}>
      <Text style={styles.comingSoonTitle}>🚀 AR Vision Guide</Text>
      <Text style={styles.comingSoonSubtitle}>Coming Soon!</Text>
      <Text style={styles.comingSoonText}>
        We're working on an amazing AR experience that will let you point your camera at monuments and get instant information overlaid in real-time.
      </Text>
      <Text style={styles.comingSoonFeatures}>
        Features in development:{'\n'}
        • Real-time landmark recognition{'\n'}
        • AR information overlay{'\n'}
        • Interactive 3D models{'\n'}
        • Historical context visualization
      </Text>
    </View>
  );
};


const styles = StyleSheet.create({
  comingSoonContainer: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
  },
  comingSoonTitle: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
    textAlign: 'center',
  },
  comingSoonSubtitle: {
    fontSize: 32,
    fontWeight: '600',
    color: '#4CAF50',
    marginBottom: 30,
    textAlign: 'center',
  },
  comingSoonText: {
    fontSize: 18,
    color: '#ccc',
    textAlign: 'center',
    lineHeight: 28,
    marginBottom: 30,
    maxWidth: 600,
  },
  comingSoonFeatures: {
    fontSize: 16,
    color: '#999',
    textAlign: 'left',
    lineHeight: 24,
    backgroundColor: 'rgba(255,255,255,0.05)',
    padding: 20,
    borderRadius: 10,
    maxWidth: 500,
  },
});

export default ARGuideScreen;