import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Dimensions, FlatList, TouchableOpacity } from 'react-native';

interface MapPin {
    id: string;
    label: string;
    lat: number;
    lon: number;
    photoCount: number;
}

export default function MapScreen() {
    const [pins, setPins] = useState<MapPin[]>([]);
    const [selectedPin, setSelectedPin] = useState<MapPin | null>(null);

    useEffect(() => {
        // Mock data - would come from diary entries
        setPins([
            { id: '1', label: 'Cairo', lat: 30.0444, lon: 31.2357, photoCount: 12 },
            { id: '2', label: 'Luxor', lat: 25.6872, lon: 32.6396, photoCount: 8 },
            { id: '3', label: 'Aswan', lat: 24.0889, lon: 32.8998, photoCount: 5 },
            { id: '4', label: 'Alexandria', lat: 31.2001, lon: 29.9187, photoCount: 3 },
        ]);
    }, []);

    const renderPin = ({ item }: { item: MapPin }) => (
        <TouchableOpacity
            style={[styles.pinCard, selectedPin?.id === item.id && styles.selectedPin]}
            onPress={() => setSelectedPin(item)}
        >
            <Text style={styles.pinIcon}>📍</Text>
            <View style={styles.pinInfo}>
                <Text style={styles.pinLabel}>{item.label}</Text>
                <Text style={styles.pinPhotos}>{item.photoCount} photos</Text>
            </View>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>🗺️ World Map</Text>
            <Text style={styles.subtitle}>Your travel memories around the globe</Text>

            {/* Placeholder for actual map - would use react-native-maps */}
            <View style={styles.mapPlaceholder}>
                <Text style={styles.mapPlaceholderText}>🌍</Text>
                <Text style={styles.mapPlaceholderLabel}>Map View</Text>
                <Text style={styles.mapPlaceholderNote}>
                    {pins.length} locations • {pins.reduce((acc, p) => acc + p.photoCount, 0)} photos
                </Text>
            </View>

            <Text style={styles.locationsTitle}>Your Locations</Text>
            <FlatList
                data={pins}
                renderItem={renderPin}
                keyExtractor={(item) => item.id}
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={{ paddingRight: 16 }}
            />

            {selectedPin && (
                <View style={styles.detailCard}>
                    <Text style={styles.detailTitle}>{selectedPin.label}</Text>
                    <Text style={styles.detailCoords}>
                        Lat: {selectedPin.lat.toFixed(4)}, Lon: {selectedPin.lon.toFixed(4)}
                    </Text>
                    <TouchableOpacity style={styles.viewButton}>
                        <Text style={styles.viewButtonText}>View {selectedPin.photoCount} Photos</Text>
                    </TouchableOpacity>
                </View>
            )}
        </View>
    );
}

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff', padding: 16 },
    title: { fontSize: 28, fontWeight: 'bold' },
    subtitle: { fontSize: 14, color: '#666', marginBottom: 16 },
    mapPlaceholder: {
        height: 250,
        backgroundColor: '#e8f4fd',
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20
    },
    mapPlaceholderText: { fontSize: 60 },
    mapPlaceholderLabel: { fontSize: 18, fontWeight: '600', color: '#1976d2', marginTop: 8 },
    mapPlaceholderNote: { fontSize: 14, color: '#666', marginTop: 4 },
    locationsTitle: { fontSize: 16, fontWeight: '600', marginBottom: 12 },
    pinCard: {
        backgroundColor: '#f5f5f5',
        borderRadius: 12,
        padding: 12,
        marginRight: 10,
        flexDirection: 'row',
        alignItems: 'center',
        minWidth: 120
    },
    selectedPin: { backgroundColor: '#e3f2fd', borderColor: '#1976d2', borderWidth: 1 },
    pinIcon: { fontSize: 20, marginRight: 8 },
    pinInfo: {},
    pinLabel: { fontSize: 14, fontWeight: '600' },
    pinPhotos: { fontSize: 12, color: '#666' },
    detailCard: { backgroundColor: '#f9f9f9', borderRadius: 12, padding: 16, marginTop: 16 },
    detailTitle: { fontSize: 20, fontWeight: 'bold' },
    detailCoords: { fontSize: 12, color: '#999', marginTop: 4 },
    viewButton: { backgroundColor: '#1976d2', borderRadius: 8, padding: 12, marginTop: 12, alignItems: 'center' },
    viewButtonText: { color: '#fff', fontWeight: '600' },
});
