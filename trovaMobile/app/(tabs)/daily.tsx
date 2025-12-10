import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, RefreshControl } from 'react-native';
import { useFocusEffect } from 'expo-router';
import client from '../../src/api/client';

interface DiaryEntry {
    id: string;
    photo_url: string;
    label: string;
    location: string;
    timestamp: string;
    confidence: number;
}

interface DayGroup {
    date: string;
    entries: DiaryEntry[];
}

export default function DailyScreen() {
    const [days, setDays] = useState<DayGroup[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    // Refresh when screen comes into focus
    useFocusEffect(
        useCallback(() => {
            fetchDiary();
        }, [])
    );

    const fetchDiary = async () => {
        try {
            // Fetch photos from storage
            const res = await client.get('/storage/photos/demo_user');
            const photos = res.data?.photos || [];

            // Group by date
            const today = new Date().toDateString();
            const yesterday = new Date(Date.now() - 86400000).toDateString();

            const grouped: { [key: string]: DiaryEntry[] } = {};

            photos.forEach((photo: any) => {
                const photoDate = photo.created_at ? new Date(photo.created_at).toDateString() : today;
                const dateLabel = photoDate === today ? 'Today' : photoDate === yesterday ? 'Yesterday' : photoDate;

                if (!grouped[dateLabel]) {
                    grouped[dateLabel] = [];
                }

                grouped[dateLabel].push({
                    id: photo.name || Math.random().toString(),
                    photo_url: photo.url || '',
                    label: photo.name?.replace('.jpg', '').replace('.png', '') || 'Photo',
                    location: 'Unknown',
                    timestamp: photo.created_at ? new Date(photo.created_at).toLocaleTimeString() : 'Unknown',
                    confidence: 0.9,
                });
            });

            // Convert to array
            const daysArray: DayGroup[] = Object.entries(grouped).map(([date, entries]) => ({
                date,
                entries: entries as DiaryEntry[],
            }));

            // If no photos, show sample
            if (daysArray.length === 0) {
                daysArray.push({
                    date: 'No photos yet',
                    entries: [{
                        id: 'sample',
                        photo_url: '',
                        label: 'Capture your first memory!',
                        location: 'Use the Capture tab',
                        timestamp: '',
                        confidence: 1.0,
                    }]
                });
            }

            setDays(daysArray);
        } catch (err) {
            console.error('Fetch diary error:', err);
            // Fallback to mock data
            setDays([
                {
                    date: 'Sample Data',
                    entries: [
                        { id: '1', photo_url: '', label: 'Karnak Temple', location: 'Luxor, Egypt', timestamp: '10:30 AM', confidence: 0.92 },
                        { id: '2', photo_url: '', label: 'Pyramids of Giza', location: 'Cairo, Egypt', timestamp: '9:00 AM', confidence: 0.95 },
                    ]
                }
            ]);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const onRefresh = () => {
        setRefreshing(true);
        fetchDiary();
    };

    const renderEntry = ({ item }: { item: DiaryEntry }) => (
        <TouchableOpacity style={styles.entryCard}>
            {item.photo_url ? (
                <Image source={{ uri: item.photo_url }} style={styles.entryPhoto} />
            ) : (
                <View style={styles.photoPlaceholder}>
                    <Text style={styles.photoIcon}>📷</Text>
                </View>
            )}
            <View style={styles.entryInfo}>
                <Text style={styles.entryLabel}>{item.label}</Text>
                <Text style={styles.entryLocation}>📍 {item.location}</Text>
                {item.timestamp && (
                    <Text style={styles.entryTime}>{item.timestamp} • {(item.confidence * 100).toFixed(0)}% confident</Text>
                )}
            </View>
        </TouchableOpacity>
    );

    const renderDay = ({ item }: { item: DayGroup }) => (
        <View style={styles.daySection}>
            <Text style={styles.dateHeader}>{item.date}</Text>
            {item.entries.map((entry) => (
                <View key={entry.id}>{renderEntry({ item: entry })}</View>
            ))}
        </View>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>📖 Daily Story</Text>
            <Text style={styles.subtitle}>Your travel memories, organized by day</Text>

            {loading ? (
                <Text style={styles.loading}>Loading timeline...</Text>
            ) : (
                <FlatList
                    data={days}
                    renderItem={renderDay}
                    keyExtractor={(item) => item.date}
                    contentContainerStyle={{ paddingBottom: 100 }}
                    refreshControl={
                        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                    }
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff', padding: 16, paddingTop: 50 },
    title: { fontSize: 28, fontWeight: 'bold', marginBottom: 4 },
    subtitle: { fontSize: 14, color: '#666', marginBottom: 20 },
    loading: { textAlign: 'center', marginTop: 50, color: '#999' },
    daySection: { marginBottom: 24 },
    dateHeader: { fontSize: 18, fontWeight: '600', color: '#333', marginBottom: 12, paddingBottom: 8, borderBottomWidth: 1, borderBottomColor: '#eee' },
    entryCard: { flexDirection: 'row', backgroundColor: '#f9f9f9', borderRadius: 12, padding: 12, marginBottom: 10 },
    photoPlaceholder: { width: 70, height: 70, backgroundColor: '#e0e0e0', borderRadius: 10, justifyContent: 'center', alignItems: 'center' },
    entryPhoto: { width: 70, height: 70, borderRadius: 10 },
    photoIcon: { fontSize: 28 },
    entryInfo: { marginLeft: 14, flex: 1, justifyContent: 'center' },
    entryLabel: { fontSize: 17, fontWeight: '600' },
    entryLocation: { fontSize: 13, color: '#666', marginTop: 3 },
    entryTime: { fontSize: 12, color: '#999', marginTop: 4 },
});
