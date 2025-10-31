import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, FlatList } from 'react-native';
import axios from 'axios';

interface ItineraryDay {
  date: string;
  activities: Array<{ id: string; title: string; start_time?: string; end_time?: string; location?: { name?: string } }>
}

const ItineraryScreen: React.FC<any> = ({ route }) => {
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState<ItineraryDay[]>([]);
  const itineraryId = route?.params?.itineraryId || 'mock-itinerary-1';

  useEffect(() => {
    const fetchItinerary = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`http://localhost:8000/api/itineraries/${itineraryId}`);
        setDays(res.data?.days || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchItinerary();
  }, [itineraryId]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Itinerary</Text>
      <FlatList
        data={days}
        keyExtractor={(item) => item.date}
        renderItem={({ item }) => (
          <View style={styles.dayCard}>
            <Text style={styles.dayTitle}>{item.date}</Text>
            {item.activities.map((act) => (
              <View key={act.id} style={styles.activityRow}>
                <Text style={styles.activityTitle}>{act.title}</Text>
                <Text style={styles.activityTime}>{[act.start_time, act.end_time].filter(Boolean).join(' - ')}</Text>
                {!!act.location?.name && <Text style={styles.activityLocation}>{act.location?.name}</Text>}
              </View>
            ))}
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  dayCard: { padding: 12, borderWidth: 1, borderColor: '#eee', borderRadius: 8, marginBottom: 12 },
  dayTitle: { fontSize: 18, fontWeight: '600', marginBottom: 8 },
  activityRow: { marginBottom: 8 },
  activityTitle: { fontSize: 16, fontWeight: '600' },
  activityTime: { fontSize: 12, color: '#555' },
  activityLocation: { fontSize: 12, color: '#777' },
});

export default ItineraryScreen;
