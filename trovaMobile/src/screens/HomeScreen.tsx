import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ImageBackground, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { colors } from '../constants/theme';
import { supabase } from '../config/supabase';
import { Ionicons } from '@expo/vector-icons';

const HomeScreen = () => {
    const router = useRouter();
    const [activeTrip, setActiveTrip] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchActiveTrip();
    }, []);

    const fetchActiveTrip = async () => {
        try {
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) return;

            const { data, error } = await supabase
                .from('trips')
                .select('*')
                .eq('user_id', user.id)
                .eq('status', 'active')
                .order('created_at', { ascending: false })
                .limit(1)
                .single();

            if (data) {
                setActiveTrip(data);
            }
        } catch (error) {
            // No active trip found is fine
        } finally {
            setLoading(false);
        }
    };

    const handleStartTrip = async () => {
        try {
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) {
                router.push('/login');
                return;
            }

            // Call backend to start trip (or direct DB insert if simpler for MVP, but let's use backend as planned)
            // For MVP speed, let's use direct Supabase insert here if backend endpoint isn't strictly required for logic
            // But we defined a backend endpoint, so let's try to use it or fallback to direct insert.
            // Direct insert is faster/easier for now.

            const { data, error } = await supabase
                .from('trips')
                .insert({
                    user_id: user.id,
                    title: `Trip to Somewhere ${new Date().toLocaleDateString()}`,
                    status: 'active'
                })
                .select()
                .single();

            if (error) throw error;
            setActiveTrip(data);
            Alert.alert('Trip Started!', 'Go to the Camera tab to start logging your journey.');
        } catch (error: any) {
            Alert.alert('Error', error.message);
        }
    };

    const handleEndTrip = async () => {
        if (!activeTrip) return;
        try {
            const { error } = await supabase
                .from('trips')
                .update({ status: 'completed', end_time: new Date().toISOString() })
                .eq('id', activeTrip.id);

            if (error) throw error;
            setActiveTrip(null);
            Alert.alert('Trip Ended', 'Your trip has been saved to your diary.');
        } catch (error: any) {
            Alert.alert('Error', error.message);
        }
    };

    return (
        <ImageBackground
            source={{ uri: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1000&auto=format&fit=crop' }}
            style={styles.container}
        >
            <View style={styles.overlay}>
                <View style={styles.header}>
                    <Text style={styles.title}>TRAVO</Text>
                    <Text style={styles.subtitle}>Automatic Travel Diary</Text>
                </View>

                <View style={styles.content}>
                    {loading ? (
                        <ActivityIndicator size="large" color="#fff" />
                    ) : activeTrip ? (
                        <View style={styles.card}>
                            <Text style={styles.cardTitle}>Current Trip</Text>
                            <Text style={styles.tripTitle}>{activeTrip.title}</Text>
                            <Text style={styles.tripDate}>Started: {new Date(activeTrip.start_time).toLocaleDateString()}</Text>

                            <View style={styles.actions}>
                                <TouchableOpacity style={styles.actionButton} onPress={() => router.push('/(tabs)/camera')}>
                                    <Ionicons name="camera" size={24} color="#fff" />
                                    <Text style={styles.actionText}>Log Moment</Text>
                                </TouchableOpacity>

                                <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]} onPress={() => router.push('/(tabs)/diary')}>
                                    <Ionicons name="book" size={24} color={colors.primary} />
                                    <Text style={[styles.actionText, styles.secondaryText]}>View Diary</Text>
                                </TouchableOpacity>
                            </View>

                            <TouchableOpacity style={styles.endButton} onPress={handleEndTrip}>
                                <Text style={styles.endButtonText}>End Trip</Text>
                            </TouchableOpacity>
                        </View>
                    ) : (
                        <View style={styles.emptyState}>
                            <Text style={styles.emptyText}>Ready for your next adventure?</Text>
                            <TouchableOpacity style={styles.startButton} onPress={handleStartTrip}>
                                <Text style={styles.startButtonText}>Start New Trip</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                </View>
            </View>
        </ImageBackground>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1 },
    overlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.4)', padding: 20, justifyContent: 'space-between' },
    header: { marginTop: 60, alignItems: 'center' },
    title: { fontSize: 42, fontWeight: '900', color: '#fff', letterSpacing: 2 },
    subtitle: { fontSize: 18, color: '#ddd', marginTop: 5 },
    content: { marginBottom: 50 },
    card: { backgroundColor: 'rgba(255,255,255,0.95)', padding: 20, borderRadius: 20, alignItems: 'center' },
    cardTitle: { fontSize: 14, color: '#666', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 },
    tripTitle: { fontSize: 24, fontWeight: 'bold', color: '#333', textAlign: 'center' },
    tripDate: { fontSize: 14, color: '#888', marginBottom: 20 },
    actions: { flexDirection: 'row', gap: 10, width: '100%', marginBottom: 15 },
    actionButton: { flex: 1, backgroundColor: colors.primary, padding: 15, borderRadius: 12, alignItems: 'center', flexDirection: 'row', justifyContent: 'center', gap: 8 },
    actionText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
    secondaryButton: { backgroundColor: '#fff', borderWidth: 1, borderColor: colors.primary },
    secondaryText: { color: colors.primary },
    endButton: { padding: 10 },
    endButtonText: { color: '#ff3b30', fontWeight: '600' },
    emptyState: { alignItems: 'center', marginBottom: 40 },
    emptyText: { color: '#fff', fontSize: 20, fontWeight: '600', marginBottom: 20, textAlign: 'center' },
    startButton: { backgroundColor: colors.primary, paddingHorizontal: 40, paddingVertical: 18, borderRadius: 30, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 5, elevation: 6 },
    startButtonText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textTransform: 'uppercase' },
});

export default HomeScreen;
