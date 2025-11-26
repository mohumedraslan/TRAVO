import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ActivityIndicator, Share, Alert } from 'react-native';
import { colors } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';
import { supabase } from '../config/supabase';
import { useRouter } from 'expo-router';

const ShareStoryScreen = () => {
    const [loading, setLoading] = useState(true);
    const [trip, setTrip] = useState<any>(null);
    const [stats, setStats] = useState({ places: 0, photos: 0 });
    const router = useRouter();

    useEffect(() => {
        fetchTripData();
    }, []);

    const fetchTripData = async () => {
        try {
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) return;

            // Get active or last trip
            const { data: tripData } = await supabase
                .from('trips')
                .select('*')
                .eq('user_id', user.id)
                .order('created_at', { ascending: false })
                .limit(1)
                .single();

            if (tripData) {
                setTrip(tripData);

                // Get stats
                const { count: placesCount } = await supabase
                    .from('trip_places')
                    .select('*', { count: 'exact', head: true })
                    .eq('trip_id', tripData.id);

                // Get photos count and a cover photo
                const { data: photos, count: photosCount } = await supabase
                    .from('trip_photos')
                    .select('photo_url', { count: 'exact' })
                    .eq('trip_place_id', (await supabase.from('trip_places').select('id').eq('trip_id', tripData.id)).data?.[0]?.id || '') // This is a bit hacky for a single query, let's simplify
                // Actually, we need to join. But for MVP let's just get a photo from the last place.

                // Better approach for stats:
                const { data: places } = await supabase
                    .from('trip_places')
                    .select('id')
                    .eq('trip_id', tripData.id);

                let totalPhotos = 0;
                let coverPhoto = 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1000&auto=format&fit=crop';

                if (places && places.length > 0) {
                    const placeIds = places.map(p => p.id);
                    const { data: tripPhotos, count } = await supabase
                        .from('trip_photos')
                        .select('photo_url', { count: 'exact' })
                        .in('trip_place_id', placeIds);

                    totalPhotos = count || 0;
                    if (tripPhotos && tripPhotos.length > 0) {
                        coverPhoto = tripPhotos[0].photo_url;
                    }
                }

                setStats({
                    places: placesCount || 0,
                    photos: totalPhotos
                });

                // Update trip object with cover photo for display
                setTrip({ ...tripData, cover_photo: coverPhoto });
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleShare = async () => {
        if (!trip) return;

        try {
            const message = `Check out my trip "${trip.title}" on Travo! I visited ${stats.places} places and took ${stats.photos} photos.`;
            await Share.share({
                message: message,
                title: `Trip to ${trip.title}`
            });
        } catch (error: any) {
            Alert.alert(error.message);
        }
    };

    if (loading) {
        return (
            <View style={styles.container}>
                <ActivityIndicator size="large" color={colors.primary} />
            </View>
        );
    }

    if (!trip) {
        return (
            <View style={styles.container}>
                <Text>No trip found.</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="#333" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Share Story</Text>
                <View style={{ width: 24 }} />
            </View>

            <View style={styles.content}>
                <Text style={styles.title}>Your Trip Summary</Text>
                <View style={styles.card}>
                    <Image
                        source={{ uri: trip.cover_photo }}
                        style={styles.previewImage}
                    />
                    <View style={styles.cardContent}>
                        <Text style={styles.tripTitle}>{trip.title}</Text>
                        <Text style={styles.date}>{new Date(trip.start_time).toLocaleDateString()}</Text>
                        <View style={styles.statsRow}>
                            <View style={styles.stat}>
                                <Ionicons name="location" size={20} color={colors.primary} />
                                <Text style={styles.statText}>{stats.places} Places</Text>
                            </View>
                            <View style={styles.stat}>
                                <Ionicons name="images" size={20} color={colors.primary} />
                                <Text style={styles.statText}>{stats.photos} Photos</Text>
                            </View>
                        </View>
                    </View>
                </View>

                <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
                    <Ionicons name="share-outline" size={24} color="#fff" />
                    <Text style={styles.shareText}>Share Story</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20 },
    headerTitle: { fontSize: 18, fontWeight: 'bold' },
    backButton: { padding: 5 },
    content: { flex: 1, padding: 20, alignItems: 'center' },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 30, alignSelf: 'flex-start' },
    card: { width: '100%', backgroundColor: '#fff', borderRadius: 20, overflow: 'hidden', marginBottom: 30, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 8, elevation: 5 },
    previewImage: { width: '100%', height: 250 },
    cardContent: { padding: 20 },
    tripTitle: { fontSize: 22, fontWeight: 'bold', marginBottom: 5 },
    date: { fontSize: 14, color: '#666', marginBottom: 15 },
    statsRow: { flexDirection: 'row', gap: 20 },
    stat: { flexDirection: 'row', alignItems: 'center', gap: 5 },
    statText: { fontSize: 16, color: '#333' },
    shareButton: { flexDirection: 'row', backgroundColor: colors.primary, paddingHorizontal: 40, paddingVertical: 15, borderRadius: 30, alignItems: 'center', gap: 10, width: '100%', justifyContent: 'center' },
    shareText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
});

export default ShareStoryScreen;
