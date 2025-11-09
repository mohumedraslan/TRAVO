import React, { useState, useEffect, useCallback } from 'react';
import { 
  View, 
  Text, 
  FlatList, 
  StyleSheet, 
  ActivityIndicator, 
  TouchableOpacity, 
  Image, 
  ScrollView,
  RefreshControl,
  ListRenderItem
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors } from '../constants/theme';

// Type definitions for navigation
type RootStackParamList = {
  Explore: undefined;
  AttractionDetail: { id: string };
  Itinerary: { attractionId: string };
};

interface Attraction {
  id: string;
  name: string;
  description: string;
  location: string;
  rating: number;
  image: string;
  categories: string[];
  isFavorite: boolean;
}

// Mock data for development
const mockAttractions: Attraction[] = [
  {
    id: '1',
    name: 'The Great Pyramid of Giza',
    description: 'The last remaining wonder of the ancient world',
    location: 'Giza, Egypt',
    rating: 4.8,
    image: 'https://example.com/pyramid.jpg',
    categories: ['Historical', 'UNESCO'],
    isFavorite: true
  },
  {
    id: '2',
    name: 'The Egyptian Museum',
    description: 'Home to an extensive collection of ancient Egyptian antiquities',
    location: 'Cairo, Egypt',
    rating: 4.5,
    image: 'https://example.com/museum.jpg',
    categories: ['Museum', 'Historical'],
    isFavorite: false
  },
  {
    id: '3',
    name: 'Khan El-Khalili',
    description: 'A major souk in the historic center of Islamic Cairo',
    location: 'Cairo, Egypt',
    rating: 4.3,
    image: 'https://example.com/khan.jpg',
    categories: ['Shopping', 'Cultural'],
    isFavorite: false
  }
];

const ExploreScreen = () => {
  const navigation = useNavigation<any>();
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [recommended, setRecommended] = useState<Attraction[]>([]);

  const loadData = async () => {
    try {
      setLoading(true);
      // TODO: Replace with actual API call
      // const destRes = await client.get('/recommendations/destinations');
      // const attrRes = await client.get('/recommendations/destinations/1/attractions');
      
      // Using mock data for now
      setAttractions(mockAttractions);
      setRecommended([...mockAttractions].sort(() => 0.5 - Math.random()).slice(0, 2));
    } catch (err) {
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  useEffect(() => {
    loadData();
  }, []);

  const toggleFavorite = useCallback((id: string) => {
    setAttractions((prev: Attraction[]) => 
      prev.map((attraction: Attraction) => 
        attraction.id === id 
          ? { ...attraction, isFavorite: !attraction.isFavorite } 
          : attraction
      )
    );
  }, []);

  const renderAttractionCard = ({ item }: { item: Attraction }) => (
    <TouchableOpacity 
      style={styles.card}
      onPress={() => navigation.navigate('attraction-detail', { id: item.id })}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.cardTitle}>{item.name}</Text>
        <TouchableOpacity onPress={() => toggleFavorite(item.id)}>
          <Ionicons 
            name={item.isFavorite ? 'heart' : 'heart-outline'} 
            size={24} 
            color={item.isFavorite ? colors.primary : '#666'} 
          />
        </TouchableOpacity>
      </View>
      <Text style={styles.cardLocation}>
        <Ionicons name="location" size={14} color={colors.primary} /> {item.location}
      </Text>
      <Text style={styles.cardDesc} numberOfLines={2}>{item.description}</Text>
      <View style={styles.ratingContainer}>
        <Ionicons name="star" size={16} color="#FFD700" />
        <Text style={styles.ratingText}>{item.rating}</Text>
        <View style={styles.categoriesContainer}>
          {item.categories.map((cat, idx) => (
            <View key={idx} style={styles.categoryTag}>
              <Text style={styles.categoryText}>{cat}</Text>
            </View>
          ))}
        </View>
      </View>
    </TouchableOpacity>
  );

  const renderRecommendedItem = ({ item }: { item: Attraction }) => (
    <TouchableOpacity 
      style={styles.recommendedCard}
      onPress={() => navigation.navigate('attraction-detail', { id: item.id })}
    >
      <View style={styles.recommendedImage}>
        <Ionicons name="image" size={40} color="#ddd" />
      </View>
      <Text style={styles.recommendedTitle} numberOfLines={1}>{item.name}</Text>
      <View style={styles.ratingContainer}>
        <Ionicons name="star" size={14} color="#FFD700" />
        <Text style={styles.smallRatingText}>{item.rating}</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading && !refreshing) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[colors.primary]}
            tintColor={colors.primary}
          />
        }
      >
        <View style={styles.headerContainer}>
          <Text style={styles.header}>Discover Egypt</Text>
          <TouchableOpacity style={styles.searchButton}>
            <Ionicons name="search" size={20} color="#666" />
          </TouchableOpacity>
        </View>

        <Text style={styles.sectionTitle}>Recommended For You</Text>
        <FlatList
          horizontal
          showsHorizontalScrollIndicator={false}
          data={recommended}
          keyExtractor={(item: Attraction) => item.id}
          contentContainerStyle={styles.recommendedList}
          renderItem={renderRecommendedItem}
        />

        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Popular Attractions</Text>
          <TouchableOpacity>
            <Text style={styles.seeAllText}>See All</Text>
          </TouchableOpacity>
        </View>

        <FlatList
          scrollEnabled={false}
          data={attractions}
          keyExtractor={(item: Attraction) => item.id}
          contentContainerStyle={styles.attractionsList}
          renderItem={renderAttractionCard}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#fff',
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  headerContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 15,
    paddingBottom: 10,
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  searchButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: '#f5f5f5',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginTop: 20,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  seeAllText: {
    color: colors.primary,
    fontSize: 14,
  },
  recommendedList: {
    paddingHorizontal: 15,
    paddingBottom: 5,
  },
  recommendedCard: {
    width: 160,
    marginRight: 15,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  recommendedImage: {
    width: '100%',
    height: 100,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  recommendedTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 5,
  },
  attractionsList: {
    paddingHorizontal: 15,
    paddingBottom: 30,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  cardLocation: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  cardDesc: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    marginLeft: 4,
    marginRight: 12,
    fontWeight: '600',
    color: '#333',
  },
  smallRatingText: {
    marginLeft: 2,
    fontSize: 12,
    color: '#666',
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginLeft: 'auto',
  },
  categoryTag: {
    backgroundColor: '#f0f7ff',
    borderRadius: 12,
    paddingVertical: 2,
    paddingHorizontal: 10,
    marginLeft: 6,
  },
  categoryText: {
    fontSize: 12,
    color: colors.primary,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
});

export default ExploreScreen;
