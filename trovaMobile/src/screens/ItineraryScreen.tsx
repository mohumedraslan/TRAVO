import * as React from 'react';
import { View, Text, StyleSheet, ActivityIndicator, FlatList, TouchableOpacity, Linking } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import client from '../api/client';

interface ItineraryDay {
  date: string;
  activities: Array<{ id: string; title: string; start_time?: string; end_time?: string; location?: { name?: string } }>
}

const ItineraryScreen: React.FC = () => {
  const [loading, setLoading] = React.useState(false);
  const [days, setDays] = React.useState<ItineraryDay[]>([]);
  const params = useLocalSearchParams();
  const router = useRouter();

  // Use param ID or fallback to mock/default
  const itineraryId = (params.itineraryId as string) || 'mock-itinerary-1';

  React.useEffect(() => {
    const fetchItinerary = async () => {
      setLoading(true);
      try {
        const res = await client.get(`/itineraries/${itineraryId}`);
        setDays(res.data?.days || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchItinerary();
  }, [itineraryId]);

  const openBooking = (query: string) => {
    const encodedQuery = encodeURIComponent(query);
    Linking.openURL(`https://www.booking.com/searchresults.html?ss=${encodedQuery}&aid=123456`);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>Itinerary</Text>
        <TouchableOpacity
          style={styles.createButton}
          onPress={() => router.push('/plan-itinerary')}
        >
          <Ionicons name="add-circle" size={24} color="#2196F3" />
          <Text style={styles.createButtonText}>New Trip</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={days}
        keyExtractor={(item) => item.date}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No itinerary found.</Text>
            <Text style={styles.emptySubtext}>Tap "New Trip" to plan your next adventure!</Text>
          </View>
        }
        renderItem={({ item }) => (
          <View style={styles.dayCard}>
            <Text style={styles.dayTitle}>{item.date}</Text>
            {item.activities.map((act: any) => (
              <View key={act.id} style={styles.activityRow}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.activityTitle}>{act.title}</Text>
                  <Text style={styles.activityTime}>{[act.start_time, act.end_time].filter(Boolean).join(' - ')}</Text>
                  {!!act.location?.name && <Text style={styles.activityLocation}>{act.location?.name}</Text>}
                </View>
                <TouchableOpacity
                  style={styles.miniBookButton}
                  onPress={() => openBooking(act.location?.name || act.title)}
                >
                  <Ionicons name="ticket-outline" size={18} color="#003580" />
                </TouchableOpacity>
              </View>
            ))}
            <TouchableOpacity
              style={styles.dayBookButton}
              onPress={() => openBooking(`Hotels in ${item.activities[0]?.location?.name || 'Egypt'}`)}
            >
              <Text style={styles.dayBookButtonText}>Book Hotels for this Day</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  header: { fontSize: 24, fontWeight: 'bold' },
  createButton: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  createButtonText: { color: '#2196F3', fontWeight: '600', fontSize: 16 },
  dayCard: { padding: 12, borderWidth: 1, borderColor: '#eee', borderRadius: 8, marginBottom: 12 },
  dayTitle: { fontSize: 18, fontWeight: '600', marginBottom: 8 },
  activityRow: { marginBottom: 8, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  activityTitle: { fontSize: 16, fontWeight: '600' },
  activityTime: { fontSize: 12, color: '#555' },
  activityLocation: { fontSize: 12, color: '#777' },
  emptyState: { padding: 20, alignItems: 'center', marginTop: 40 },
  emptyText: { fontSize: 18, color: '#333', marginBottom: 8 },
  emptySubtext: { fontSize: 14, color: '#666', textAlign: 'center' },
  miniBookButton: { padding: 8 },
  dayBookButton: { marginTop: 8, padding: 10, backgroundColor: '#f0f7ff', borderRadius: 6, alignItems: 'center' },
  dayBookButtonText: { color: '#003580', fontWeight: '600', fontSize: 14 },
});

export default ItineraryScreen;
