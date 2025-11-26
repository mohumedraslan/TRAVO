import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, RefreshControl, ActivityIndicator } from 'react-native';
import { supabase } from '../config/supabase';
import { colors } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';

const DiaryScreen = () => {
    const [timeline, setTimeline] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        fetchTimeline();
    }, []);

    const fetchTimeline = async () => {
        try {
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) return;

            // Get active trip first (or most recent)
            const { data: trip } = await supabase
                .from('trips')
                .select('id')
                .eq('user_id', user.id)
                .order('created_at', { ascending: false })
                .limit(1)
                .single();

            if (trip) {
                // Fetch places and photos for this trip
                // Note: This is a simplified fetch. Ideally we use the backend endpoint /api/diary/{trip_id}/timeline
                // But for direct Supabase access:
                const { data: places, error } = await supabase
                    .from('trip_places')
                    .select('*, trip_photos(*)')
                    .eq('trip_id', trip.id)
                    .order('created_at', { ascending: false }); // Newest first

                if (error) throw error;
                setTimeline(places || []);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const onRefresh = () => {
        setRefreshing(true);
        fetchTimeline();
    };

    const renderItem = ({ item }: { item: any }) => (
        <View style={styles.timelineItem}>
            <View style={styles.timelineLeft}>
                <View style={styles.line} />
                <View style={styles.dot} />
            </View>
            <View style={styles.content}>
                <Text style={styles.time}>{new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</Text>
                <Text style={styles.placeName}>{item.place_name}</Text>
                {item.address && <Text style={styles.address}>{item.address}</Text>}

                {item.trip_photos && item.trip_photos.length > 0 && (
                    <View style={styles.photosContainer}>
                        {item.trip_photos.map((photo: any) => (
                            <Image key={photo.id} source={{ uri: photo.photo_url }} style={styles.photo} />
                        ))}
                    </View>
                )}
            </View>
        </View>
    );

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Travel Diary</Text>
            </View>

            {loading ? (
                <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 50 }} />
            ) : timeline.length === 0 ? (
                <View style={styles.emptyState}>
                    <Ionicons name="book-outline" size={64} color="#ccc" />
                    <Text style={styles.emptyText}>No moments logged yet.</Text>
                    <Text style={styles.emptySubtext}>Start a trip and take photos to build your diary.</Text>
                </View>
            ) : (
                <FlatList
                    data={timeline}
                    renderItem={renderItem}
                    keyExtractor={(item) => item.id}
                    contentContainerStyle={styles.listContent}
                    refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
                />
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    header: { paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
    headerTitle: { fontSize: 28, fontWeight: 'bold', color: '#333' },
    listContent: { padding: 20 },
    timelineItem: { flexDirection: 'row', marginBottom: 30 },
    timelineLeft: { alignItems: 'center', marginRight: 15, width: 20 },
    line: { position: 'absolute', top: 0, bottom: -30, width: 2, backgroundColor: '#eee' },
    dot: { width: 12, height: 12, borderRadius: 6, backgroundColor: colors.primary, marginTop: 5 },
    content: { flex: 1, backgroundColor: '#f9f9f9', padding: 15, borderRadius: 12 },
    time: { fontSize: 12, color: '#999', marginBottom: 4 },
    placeName: { fontSize: 18, fontWeight: 'bold', color: '#333', marginBottom: 4 },
    address: { fontSize: 14, color: '#666', marginBottom: 10 },
    photosContainer: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
    photo: { width: '100%', height: 200, borderRadius: 8, backgroundColor: '#eee' },
    emptyState: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 40 },
    emptyText: { fontSize: 18, fontWeight: '600', color: '#666', marginTop: 20 },
    emptySubtext: { fontSize: 14, color: '#999', textAlign: 'center', marginTop: 10 },
});

export default DiaryScreen;
