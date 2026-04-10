import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, TouchableOpacity, Image, Dimensions } from 'react-native';
import MapView, { Marker, Callout, PROVIDER_GOOGLE } from 'react-native-maps';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../constants/theme';

// Mock data - in real app, fetch from backend
const monuments = [
    { id: '1', name: 'Pyramids of Giza', latitude: 29.9792, longitude: 31.1342, image: 'https://images.unsplash.com/photo-1539650116455-8efdb4f85381?q=80&w=1000&auto=format&fit=crop' },
    { id: '2', name: 'Great Sphinx', latitude: 29.9753, longitude: 31.1376, image: 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?q=80&w=1000&auto=format&fit=crop' },
    { id: '3', name: 'Karnak Temple', latitude: 25.7188, longitude: 32.6573, image: 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=1000&auto=format&fit=crop' },
    { id: '4', name: 'Abu Simbel', latitude: 22.3372, longitude: 31.6258, image: 'https://images.unsplash.com/photo-1574236170880-4398d11b9538?q=80&w=1000&auto=format&fit=crop' },
    { id: '5', name: 'Valley of the Kings', latitude: 25.7402, longitude: 32.6014, image: 'https://images.unsplash.com/photo-1544427920-c49ccfb85579?q=80&w=1000&auto=format&fit=crop' },
];

const MapScreen = () => {
    const router = useRouter();
    const [selectedMonument, setSelectedMonument] = useState<any>(null);

    const initialRegion = {
        latitude: 26.8206,
        longitude: 30.8025,
        latitudeDelta: 10,
        longitudeDelta: 10,
    };

    return (
        <View style={styles.container}>
            <MapView
                style={styles.map}
                initialRegion={initialRegion}
                provider={PROVIDER_GOOGLE}
            >
                {monuments.map((monument) => (
                    <Marker
                        key={monument.id}
                        coordinate={{ latitude: monument.latitude, longitude: monument.longitude }}
                        title={monument.name}
                        onPress={() => setSelectedMonument(monument)}
                    >
                        <Callout tooltip onPress={() => router.push({ pathname: '/attraction-detail', params: { id: monument.id } })}>
                            <View style={styles.calloutContainer}>
                                <Text style={styles.calloutTitle}>{monument.name}</Text>
                                <Image source={{ uri: monument.image }} style={styles.calloutImage} />
                                <TouchableOpacity style={styles.calloutButton}>
                                    <Text style={styles.calloutButtonText}>View Details</Text>
                                </TouchableOpacity>
                            </View>
                        </Callout>
                    </Marker>
                ))}
            </MapView>

            {/* Floating Back Button if needed, or just rely on tabs */}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    map: {
        width: Dimensions.get('window').width,
        height: Dimensions.get('window').height,
    },
    calloutContainer: {
        width: 200,
        backgroundColor: 'white',
        borderRadius: 8,
        padding: 10,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    calloutTitle: {
        fontWeight: 'bold',
        marginBottom: 5,
        textAlign: 'center',
    },
    calloutImage: {
        width: 180,
        height: 100,
        borderRadius: 4,
        marginBottom: 5,
    },
    calloutButton: {
        backgroundColor: colors.primary,
        paddingVertical: 5,
        paddingHorizontal: 10,
        borderRadius: 4,
        marginTop: 5,
    },
    calloutButtonText: {
        color: 'white',
        fontSize: 12,
        fontWeight: 'bold',
    },
});

export default MapScreen;
