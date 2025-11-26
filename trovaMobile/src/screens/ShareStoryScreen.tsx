import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { colors } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';

const ShareStoryScreen = () => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>Share Your Story</Text>
            <View style={styles.card}>
                <Image
                    source={{ uri: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1000&auto=format&fit=crop' }}
                    style={styles.previewImage}
                />
                <Text style={styles.tripTitle}>My Amazing Trip</Text>
                <Text style={styles.stats}>12 Places • 45 Photos</Text>
            </View>

            <TouchableOpacity style={styles.shareButton}>
                <Ionicons name="share-outline" size={24} color="#fff" />
                <Text style={styles.shareText}>Share Story</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, alignItems: 'center', justifyContent: 'center', backgroundColor: '#fff' },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 30 },
    card: { width: '100%', backgroundColor: '#f5f5f5', borderRadius: 20, overflow: 'hidden', marginBottom: 30 },
    previewImage: { width: '100%', height: 300 },
    tripTitle: { fontSize: 22, fontWeight: 'bold', padding: 15, paddingBottom: 5 },
    stats: { fontSize: 14, color: '#666', paddingHorizontal: 15, paddingBottom: 20 },
    shareButton: { flexDirection: 'row', backgroundColor: colors.primary, paddingHorizontal: 40, paddingVertical: 15, borderRadius: 30, alignItems: 'center', gap: 10 },
    shareText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
});

export default ShareStoryScreen;
