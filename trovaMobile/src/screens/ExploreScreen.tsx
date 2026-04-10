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
import { API_BASE_URL } from '../api/client';
import { useNavigation, useRouter } from 'expo-router';
import { colors } from '../constants/theme';

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

const ExploreScreen = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [recommended, setRecommended] = useState<Attraction[]>([]);
  const placeholder = 'https://via.placeholder.com/800x600?text=Image+Unavailable';

  const loadData = async () => {
    try {
      setLoading(true);
      // Mock data with remote images for now to ensure they load
      const files = [
        { id: '1', name: 'Pyramids of Giza', image: 'https://images.unsplash.com/photo-1539650116455-8efdb4f85381?q=80&w=1000&auto=format&fit=crop', location: 'Giza, Egypt', rating: 4.8, categories: ['Historical', 'UNESCO'] },
        { id: '2', name: 'Great Sphinx', image: 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?q=80&w=1000&auto=format&fit=crop', location: 'Giza, Egypt', rating: 4.6, categories: ['Historical'] },
        { id: '3', name: 'Karnak Temple', image: 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?q=80&w=1000&auto=format&fit=crop', location: 'Luxor, Egypt', rating: 4.9, categories: ['UNESCO', 'Cultural'] },
        { id: '4', name: 'Abu Simbel', image: 'https://images.unsplash.com/photo-1574236170880-4398d11b9538?q=80&w=1000&auto=format&fit=crop', location: 'Aswan, Egypt', rating: 4.7, categories: ['Monument'] },
        { id: '5', name: 'Valley of the Kings', image: 'https://images.unsplash.com/photo-1544427920-c49ccfb85579?q=80&w=1000&auto=format&fit=crop', location: 'Luxor, Egypt', rating: 4.8, categories: ['Scenic'] },
      ];

      const built: Attraction[] = files.map((f) => ({
        id: f.id,
        name: f.name,
        description: `Discover ${f.name}.`,
        location: f.location,
        rating: f.rating,
        image: f.image,
        categories: f.categories,
        isFavorite: false,
      }));
      setAttractions(built);
      setRecommended(built.slice(0, 3));
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

  const handlePlanVisit = (attraction: Attraction) => {
    router.push('/(tabs)/itinerary');
  };

  const renderAttractionCard = ({ item }: { item: Attraction }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => router.push({ pathname: '/attraction-detail', params: { id: item.id } })}
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
      <Image
        source={{ uri: item.image }}
        style={styles.cardImage}
        resizeMode="cover"
      />
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
      <TouchableOpacity style={styles.planButton} onPress={() => handlePlanVisit(item)}>
        <Text style={styles.planButtonText}>Plan Visit</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );

  const renderRecommendedItem = ({ item }: { item: Attraction }) => (
    <TouchableOpacity
      style={styles.recommendedCard}
      onPress={() => router.push({ pathname: '/attraction-detail', params: { id: item.id } })}
    >
      <Image
        source={{ uri: item.image }}
        style={styles.recommendedImage}
        resizeMode="cover"
      />
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
    marginLeft: 20,
    marginBottom: 10,
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
  cardImage: {
    width: '100%',
    height: 180,
    borderRadius: 8,
    marginBottom: 10,
    backgroundColor: '#f5f5f5',
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
    marginBottom: 12,
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
  planButton: {
    backgroundColor: colors.primary,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 5,
  },
  planButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
});

export default ExploreScreen;
