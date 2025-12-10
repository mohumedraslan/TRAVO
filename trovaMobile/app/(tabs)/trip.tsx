import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, Alert, TextInput, Modal } from 'react-native';
import * as Location from 'expo-location';

interface Trip {
    id: string;
    name: string;
    startDate: string;
    endDate?: string;
    photoCount: number;
    isActive: boolean;
}

export default function TripScreen() {
    const [trips, setTrips] = useState<Trip[]>([]);
    const [activeTrip, setActiveTrip] = useState<Trip | null>(null);
    const [location, setLocation] = useState<string>('Detecting...');
    const [showNewTripModal, setShowNewTripModal] = useState(false);
    const [newTripName, setNewTripName] = useState('');

    useEffect(() => {
        loadTrips();
        getLocation();
    }, []);

    const getLocation = async () => {
        try {
            const { status } = await Location.requestForegroundPermissionsAsync();
            if (status === 'granted') {
                const loc = await Location.getCurrentPositionAsync({});
                const [addr] = await Location.reverseGeocodeAsync(loc.coords);
                if (addr) {
                    setLocation(`${addr.city || addr.region}, ${addr.country}`);
                }
            }
        } catch {
            setLocation('Unknown Location');
        }
    };

    const loadTrips = () => {
        setTrips([
            { id: '1', name: 'Egypt Adventure', startDate: '2024-12-01', photoCount: 24, isActive: true },
            { id: '2', name: 'Paris Weekend', startDate: '2024-11-15', endDate: '2024-11-18', photoCount: 48, isActive: false },
        ]);
        setActiveTrip({ id: '1', name: 'Egypt Adventure', startDate: '2024-12-01', photoCount: 24, isActive: true });
    };

    const startNewTrip = () => {
        if (!newTripName.trim()) return;

        const newTrip: Trip = {
            id: Date.now().toString(),
            name: newTripName,
            startDate: new Date().toISOString().split('T')[0],
            photoCount: 0,
            isActive: true,
        };
        setTrips([newTrip, ...trips.map(t => ({ ...t, isActive: false }))]);
        setActiveTrip(newTrip);
        setShowNewTripModal(false);
        setNewTripName('');
        Alert.alert('Trip Started!', `${newTripName} is now active.`);
    };

    const endTrip = () => {
        if (activeTrip) {
            Alert.alert('End Trip', `End "${activeTrip.name}"?`, [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'End Trip',
                    onPress: () => {
                        setTrips(trips.map(t =>
                            t.id === activeTrip.id
                                ? { ...t, isActive: false, endDate: new Date().toISOString().split('T')[0] }
                                : t
                        ));
                        setActiveTrip(null);
                    }
                }
            ]);
        }
    };

    const renderTrip = ({ item }: { item: Trip }) => (
        <TouchableOpacity style={[styles.tripCard, item.isActive && styles.activeCard]}>
            <View style={styles.tripHeader}>
                <Text style={styles.tripName}>{item.name}</Text>
                {item.isActive && <Text style={styles.activeBadge}>ACTIVE</Text>}
            </View>
            <Text style={styles.tripDates}>
                {item.startDate} {item.endDate ? `→ ${item.endDate}` : '→ Ongoing'}
            </Text>
            <Text style={styles.photoCount}>📸 {item.photoCount} photos</Text>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>🌍 Trips</Text>
            <Text style={styles.location}>📍 {location}</Text>

            {activeTrip ? (
                <View style={styles.activeSection}>
                    <Text style={styles.sectionTitle}>Current Trip</Text>
                    <View style={styles.currentTrip}>
                        <Text style={styles.currentName}>{activeTrip.name}</Text>
                        <Text style={styles.currentDate}>Started: {activeTrip.startDate}</Text>
                        <Text style={styles.currentPhotos}>📸 {activeTrip.photoCount} photos</Text>
                        <TouchableOpacity style={styles.endButton} onPress={endTrip}>
                            <Text style={styles.endButtonText}>End Trip</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            ) : (
                <TouchableOpacity style={styles.startButton} onPress={() => setShowNewTripModal(true)}>
                    <Text style={styles.startButtonText}>+ Start New Trip</Text>
                </TouchableOpacity>
            )}

            <Text style={styles.sectionTitle}>Past Trips</Text>
            <FlatList
                data={trips.filter(t => !t.isActive)}
                renderItem={renderTrip}
                keyExtractor={(item) => item.id}
                contentContainerStyle={{ paddingBottom: 100 }}
                ListEmptyComponent={<Text style={styles.emptyText}>No past trips yet</Text>}
            />

            {/* New Trip Modal */}
            <Modal visible={showNewTripModal} animationType="slide" transparent>
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <Text style={styles.modalTitle}>Start New Trip</Text>
                        <TextInput
                            style={styles.input}
                            placeholder="Trip name (e.g., Egypt Adventure)"
                            value={newTripName}
                            onChangeText={setNewTripName}
                            autoFocus
                        />
                        <View style={styles.modalButtons}>
                            <TouchableOpacity style={styles.cancelButton} onPress={() => setShowNewTripModal(false)}>
                                <Text style={styles.cancelButtonText}>Cancel</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.createButton} onPress={startNewTrip}>
                                <Text style={styles.createButtonText}>Start Trip</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff', padding: 16, paddingTop: 50 },
    title: { fontSize: 28, fontWeight: 'bold' },
    location: { fontSize: 14, color: '#666', marginBottom: 20 },
    activeSection: { marginBottom: 24 },
    sectionTitle: { fontSize: 16, fontWeight: '600', color: '#333', marginBottom: 12 },
    currentTrip: { backgroundColor: '#e8f5e9', borderRadius: 12, padding: 16 },
    currentName: { fontSize: 20, fontWeight: 'bold', color: '#2e7d32' },
    currentDate: { fontSize: 14, color: '#666', marginTop: 4 },
    currentPhotos: { fontSize: 14, color: '#2e7d32', marginTop: 4 },
    endButton: { backgroundColor: '#ff5722', borderRadius: 8, padding: 12, marginTop: 12, alignItems: 'center' },
    endButtonText: { color: '#fff', fontWeight: '600' },
    startButton: { backgroundColor: '#2196f3', borderRadius: 12, padding: 18, alignItems: 'center', marginBottom: 24 },
    startButtonText: { color: '#fff', fontSize: 18, fontWeight: '600' },
    tripCard: { backgroundColor: '#f5f5f5', borderRadius: 12, padding: 16, marginBottom: 12 },
    activeCard: { backgroundColor: '#e3f2fd', borderColor: '#2196f3', borderWidth: 1 },
    tripHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
    tripName: { fontSize: 18, fontWeight: '600' },
    activeBadge: { backgroundColor: '#4caf50', color: '#fff', fontSize: 10, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 4, overflow: 'hidden' },
    tripDates: { fontSize: 13, color: '#666', marginTop: 4 },
    photoCount: { fontSize: 13, color: '#999', marginTop: 4 },
    emptyText: { textAlign: 'center', color: '#999', marginTop: 20 },
    // Modal styles
    modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', padding: 20 },
    modalContent: { backgroundColor: '#fff', borderRadius: 16, padding: 24 },
    modalTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 16 },
    input: { backgroundColor: '#f5f5f5', borderRadius: 10, padding: 14, fontSize: 16 },
    modalButtons: { flexDirection: 'row', marginTop: 20, gap: 12 },
    cancelButton: { flex: 1, padding: 14, alignItems: 'center', borderRadius: 10, backgroundColor: '#f0f0f0' },
    cancelButtonText: { color: '#666', fontWeight: '600' },
    createButton: { flex: 1, padding: 14, alignItems: 'center', borderRadius: 10, backgroundColor: '#2196f3' },
    createButtonText: { color: '#fff', fontWeight: '600' },
});
