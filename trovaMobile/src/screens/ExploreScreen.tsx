import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import axios from 'axios';

interface Attraction {
  id: string;
  name: string;
  description?: string;
  categories?: string[];
}

const ExploreScreen: React.FC<any> = ({ navigation }) => {
  const [loading, setLoading] = useState(false);
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [recommended, setRecommended] = useState<Attraction[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const destRes = await axios.get('http://localhost:8000/api/recommendations/destinations');
        const attrRes = await axios.get('http://localhost:8000/api/recommendations/destinations/1/attractions');
        setAttractions(attrRes.data?.items || []);
        setRecommended(destRes.data?.items || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Explore</Text>

      <Text style={styles.subheader}>Recommended Destinations</Text>
      <FlatList
        horizontal
        data={recommended}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ paddingVertical: 8 }}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>{item.name}</Text>
            <Text style={styles.cardDesc}>{item.description || 'Beautiful destination'}</Text>
          </View>
        )}
      />

      <Text style={styles.subheader}>Attractions</Text>
      <FlatList
        data={attractions}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.listItem} onPress={() => navigation.navigate('Itinerary', { attractionId: item.id })}>
            <Text style={styles.itemTitle}>{item.name}</Text>
            <Text style={styles.itemDesc}>{item.description || 'Top attraction'}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  subheader: { fontSize: 18, fontWeight: '600', marginVertical: 8 },
  card: { padding: 12, marginRight: 12, borderWidth: 1, borderColor: '#eee', borderRadius: 8, width: 200 },
  cardTitle: { fontSize: 16, fontWeight: '600' },
  cardDesc: { fontSize: 12, color: '#555' },
  listItem: { padding: 12, borderBottomWidth: 1, borderColor: '#eee' },
  itemTitle: { fontSize: 16, fontWeight: '600' },
  itemDesc: { fontSize: 12, color: '#555' },
});

export default ExploreScreen;
