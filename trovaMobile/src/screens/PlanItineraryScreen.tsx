import * as React from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import client from '../api/client';

const INTERESTS = ['History', 'Art', 'Food', 'Nature', 'Adventure', 'Shopping'];
const DURATIONS = [1, 3, 5, 7];

export default function PlanItineraryScreen() {
    const router = useRouter();
    const params = useLocalSearchParams();

    const [destination, setDestination] = React.useState((params.destination as string) || 'Cairo, Egypt');
    const [duration, setDuration] = React.useState(3);
    const [selectedInterests, setSelectedInterests] = React.useState<string[]>(
        params.interest ? [(params.interest as string)] : []
    );
    const [loading, setLoading] = React.useState(false);

    const toggleInterest = (interest: string) => {
        if (selectedInterests.includes(interest)) {
            setSelectedInterests(selectedInterests.filter((i: string) => i !== interest));
        } else {
            setSelectedInterests([...selectedInterests, interest]);
        }
    };

    const generateItinerary = async () => {
        if (!destination.trim()) {
            Alert.alert('Error', 'Please enter a destination');
            return;
        }

        setLoading(true);
        try {
            // Calculate dates based on duration
            const startDate = new Date();
            const endDate = new Date();
            endDate.setDate(startDate.getDate() + duration);

            const response = await client.post('/itineraries/generate', {
                destination,
                start_date: startDate.toISOString(),
                end_date: endDate.toISOString(),
                preferences: selectedInterests,
                budget_level: 'moderate',
                user_id: 'user_123' // Hardcoded for demo
            });

            if (response.data) {
                // Navigate to the itinerary screen with the new itinerary ID
                router.replace({
                    pathname: '/(tabs)/itinerary',
                    params: { itineraryId: response.data.id }
                });
            }
        } catch (error: any) {
            console.error('Error generating itinerary:', error);
            Alert.alert('Error', 'Failed to generate itinerary. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScrollView style={styles.container} contentContainerStyle={styles.content}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="#333" />
                </TouchableOpacity>
                <Text style={styles.title}>Plan Your Trip</Text>
            </View>

            <View style={styles.section}>
                <Text style={styles.label}>Where to?</Text>
                <View style={styles.inputContainer}>
                    <Ionicons name="location-outline" size={20} color="#666" />
                    <TextInput
                        style={styles.input}
                        value={destination}
                        onChangeText={setDestination}
                        placeholder="e.g. Cairo, Egypt"
                    />
                </View>
            </View>

            <View style={styles.section}>
                <Text style={styles.label}>Duration (Days)</Text>
                <View style={styles.chipsContainer}>
                    {DURATIONS.map(d => (
                        <TouchableOpacity
                            key={d}
                            style={[styles.chip, duration === d && styles.activeChip]}
                            onPress={() => setDuration(d)}
                        >
                            <Text style={[styles.chipText, duration === d && styles.activeChipText]}>
                                {d} Day{d > 1 ? 's' : ''}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            <View style={styles.section}>
                <Text style={styles.label}>Interests</Text>
                <View style={styles.chipsContainer}>
                    {INTERESTS.map(interest => (
                        <TouchableOpacity
                            key={interest}
                            style={[
                                styles.chip,
                                selectedInterests.includes(interest) && styles.activeChip
                            ]}
                            onPress={() => toggleInterest(interest)}
                        >
                            <Text style={[
                                styles.chipText,
                                selectedInterests.includes(interest) && styles.activeChipText
                            ]}>
                                {interest}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            <TouchableOpacity
                style={[styles.generateButton, loading && styles.disabledButton]}
                onPress={generateItinerary}
                disabled={loading}
            >
                {loading ? (
                    <ActivityIndicator color="#fff" />
                ) : (
                    <>
                        <Ionicons name="sparkles" size={20} color="#fff" style={{ marginRight: 8 }} />
                        <Text style={styles.generateButtonText}>Generate Itinerary</Text>
                    </>
                )}
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    content: { padding: 20 },
    header: { flexDirection: 'row', alignItems: 'center', marginBottom: 30, marginTop: 10 },
    backButton: { padding: 8, marginRight: 10 },
    title: { fontSize: 24, fontWeight: 'bold', color: '#333' },
    section: { marginBottom: 24 },
    label: { fontSize: 16, fontWeight: '600', color: '#333', marginBottom: 12 },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#f5f5f5',
        borderRadius: 12,
        paddingHorizontal: 16,
        paddingVertical: 12,
    },
    input: { flex: 1, marginLeft: 10, fontSize: 16, color: '#333' },
    chipsContainer: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
    chip: {
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: '#f0f0f0',
        borderWidth: 1,
        borderColor: 'transparent',
    },
    activeChip: {
        backgroundColor: '#e3f2fd',
        borderColor: '#2196F3',
    },
    chipText: { fontSize: 14, color: '#666' },
    activeChipText: { color: '#2196F3', fontWeight: '600' },
    generateButton: {
        backgroundColor: '#2196F3',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 16,
        borderRadius: 12,
        marginTop: 20,
        shadowColor: '#2196F3',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 4,
    },
    disabledButton: { opacity: 0.7 },
    generateButtonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
});
