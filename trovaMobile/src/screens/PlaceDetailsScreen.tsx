import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { colors } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';

const PlaceDetailsScreen = () => {
    const { id, name, image, description } = useLocalSearchParams();
    const router = useRouter();

    return (
        <ScrollView style={styles.container}>
            <Image source={{ uri: image as string }} style={styles.image} />

            <View style={styles.content}>
                <Text style={styles.title}>{name}</Text>
                <Text style={styles.description}>
                    {description || "No description available for this place."}
                </Text>

                <View style={styles.meta}>
                    <View style={styles.metaItem}>
                        <Ionicons name="time-outline" size={20} color="#666" />
                        <Text style={styles.metaText}>Visited today</Text>
                    </View>
                    <View style={styles.metaItem}>
                        <Ionicons name="location-outline" size={20} color="#666" />
                        <Text style={styles.metaText}>GPS Location</Text>
                    </View>
                </View>

                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <Text style={styles.backButtonText}>Back to Diary</Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    image: { width: '100%', height: 300 },
    content: { padding: 20 },
    title: { fontSize: 28, fontWeight: 'bold', marginBottom: 10, color: '#333' },
    description: { fontSize: 16, lineHeight: 24, color: '#666', marginBottom: 20 },
    meta: { flexDirection: 'row', gap: 20, marginBottom: 30 },
    metaItem: { flexDirection: 'row', alignItems: 'center', gap: 5 },
    metaText: { color: '#666' },
    backButton: { backgroundColor: colors.primary, padding: 15, borderRadius: 10, alignItems: 'center' },
    backButtonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});

export default PlaceDetailsScreen;
