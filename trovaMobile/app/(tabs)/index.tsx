import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, Modal, FlatList, ActivityIndicator, Image, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { BlurView } from 'expo-blur'; // Note: might need install if used, but sticking to solid for now to be safe
import client from '../../src/api/client';

const { width } = Dimensions.get('window');

interface SearchResult {
  id: string;
  type: string;
  title: string;
  subtitle: string;
  image_url?: string;
}

export default function HomeScreen() {
  const router = useRouter();
  const [searchVisible, setSearchVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [userName, setUserName] = useState("Traveler");

  useEffect(() => {
    // Mock fetching user name
    AsyncStorage.getItem('isGuest').then(guest => {
      if (guest === 'true') setUserName("Guest");
      else setUserName("Traveler"); // Could fetch real name
    });
  }, []);


  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const isGuest = await AsyncStorage.getItem('isGuest');
      const userId = (isGuest === 'true') ? 'anonymous' : (await AsyncStorage.getItem('userId')) || 'anonymous';

      const res = await client.post('/assistant/query', {
        query: searchQuery,
        user_id: userId
      });

      setSearchResults(res.data.results || []);
    } catch (err) {
      console.error(err);
    } finally {
      setSearching(false);
    }
  };

  const quickActions = [
    { icon: 'camera-outline', label: 'Capture', route: '/camera', color: '#4CAF50' },
    { icon: 'airplane-outline', label: 'Trips', route: '/trip', color: '#2196F3' },
    { icon: 'book-outline', label: 'Journal', route: '/daily', color: '#FF9800' },
    { icon: 'map-outline', label: 'Map', route: '/map', color: '#9C27B0' },
  ];

  return (
    <View style={styles.container}>
      {/* HERO SECTION */}
      <LinearGradient
        colors={['#0f0c29', '#302b63', '#24243e']}
        style={styles.heroGradient}
      >
        <View style={styles.heroContent}>
          <View>
            <Text style={styles.greetingSub}>Good Morning,</Text>
            <Text style={styles.greetingName}>{userName}</Text>
          </View>
          <TouchableOpacity style={styles.profileButton} onPress={() => router.push('/settings')}>
            <Ionicons name="person-circle-outline" size={40} color="#fff" />
          </TouchableOpacity>
        </View>

        {/* FLOATING SEARCH BAR */}
        <TouchableOpacity style={styles.searchBar} onPress={() => setSearchVisible(true)}>
          <Ionicons name="search" size={20} color="#666" style={{ marginRight: 10 }} />
          <Text style={styles.searchPlaceholder}>Find your memories...</Text>
        </TouchableOpacity>
      </LinearGradient>

      <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>

        {/* ACTION GRID */}
        <View style={styles.gridContainer}>
          {quickActions.map((action, i) => (
            <TouchableOpacity
              key={i}
              style={styles.gridItem}
              onPress={() => router.push(action.route as any)}
            >
              <View style={[styles.iconCircle, { backgroundColor: action.color + '20' }]}>
                <Ionicons name={action.icon as any} size={28} color={action.color} />
              </View>
              <Text style={styles.gridLabel}>{action.label}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* ACTIVE TRIP CARD */}
        <TouchableOpacity style={styles.tripCard} onPress={() => router.push('/trip')}>
          <LinearGradient
            colors={['rgba(0,0,0,0.1)', 'rgba(0,0,0,0.8)']}
            style={styles.tripGradient}
          >
            <View style={styles.tripContent}>
              <View style={styles.liveTag}>
                <View style={styles.pulseDot} />
                <Text style={styles.liveText}>LIVE</Text>
              </View>
              <View>
                <Text style={styles.tripTitle}>Egypt Adventure</Text>
                <Text style={styles.tripSubtitle}>Day 5 • Cairo, Egypt</Text>
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* RECENT MEMORIES */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Recent Memories</Text>
          <TouchableOpacity>
            <Text style={styles.seeAll}>See All</Text>
          </TouchableOpacity>
        </View>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.memoriesRail} contentContainerStyle={{ paddingRight: 20 }}>
          {[1, 2, 3, 4].map((_, i) => (
            <View key={i} style={styles.memoryItem}>
              <Ionicons name="image-outline" size={30} color="#ccc" />
            </View>
          ))}
        </ScrollView>

        <View style={{ height: 100 }} />
      </ScrollView>

      {/* SEARCH MODAL */}
      <Modal visible={searchVisible} animationType="slide" transparent>
        <BlurView intensity={90} tint="light" style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Search Memories</Text>
              <TouchableOpacity onPress={() => setSearchVisible(false)}>
                <Ionicons name="close-circle" size={28} color="#666" />
              </TouchableOpacity>
            </View>

            <View style={styles.modalInputWrapper}>
              <Ionicons name="search" size={20} color="#666" />
              <TextInput
                style={styles.modalInput}
                placeholder="Type 'Coffee in Paris'..."
                value={searchQuery}
                onChangeText={setSearchQuery}
                onSubmitEditing={handleSearch}
                autoFocus
              />
              {searching && <ActivityIndicator size="small" color="#007AFF" />}
            </View>

            <FlatList
              data={searchResults}
              keyExtractor={(item) => item.id}
              contentContainerStyle={{ marginTop: 20 }}
              renderItem={({ item }) => (
                <TouchableOpacity style={styles.resultItem}>
                  <View style={styles.resultIcon}>
                    <Ionicons name={item.type === 'trip' ? "airplane" : "image"} size={20} color="#555" />
                  </View>
                  <View>
                    <Text style={styles.resultTitle}>{item.title}</Text>
                    <Text style={styles.resultSubtitle}>{item.subtitle}</Text>
                  </View>
                </TouchableOpacity>
              )}
            />
          </View>
        </BlurView>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },

  // HERO
  heroGradient: { paddingTop: 60, paddingBottom: 40, paddingHorizontal: 24, borderBottomLeftRadius: 30, borderBottomRightRadius: 30 },
  heroContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 },
  greetingSub: { fontSize: 16, color: '#rgba(255,255,255,0.8)', fontWeight: '500' },
  greetingName: { fontSize: 28, color: '#fff', fontWeight: 'bold' },
  profileButton: { padding: 4 },

  // SEARCH
  searchBar: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 16, padding: 14, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 10, elevation: 5 },
  searchPlaceholder: { color: '#666', fontSize: 16 },

  scrollContent: { marginTop: 24, paddingHorizontal: 20 },

  // GRID
  gridContainer: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 24 },
  gridItem: { width: '48%', backgroundColor: '#fff', padding: 16, borderRadius: 20, marginBottom: 16, alignItems: 'center', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, elevation: 2 },
  iconCircle: { width: 50, height: 50, borderRadius: 25, justifyContent: 'center', alignItems: 'center', marginBottom: 12 },
  gridLabel: { fontSize: 15, fontWeight: '600', color: '#333' },

  // TRIP CARD
  tripCard: { height: 180, borderRadius: 24, overflow: 'hidden', marginBottom: 32, backgroundColor: '#333', elevation: 4 },
  tripGradient: { flex: 1, padding: 20, justifyContent: 'space-between' },
  liveTag: { alignSelf: 'flex-start', backgroundColor: '#dc3545', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, flexDirection: 'row', alignItems: 'center' },
  pulseDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#fff', marginRight: 6 },
  liveText: { color: '#fff', fontSize: 10, fontWeight: 'bold' },
  tripContent: { justifyContent: 'space-between', flex: 1 },
  tripTitle: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginTop: 'auto' },
  tripSubtitle: { fontSize: 14, color: 'rgba(255,255,255,0.8)', marginTop: 4 },

  // MEMORIES
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  sectionTitle: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  seeAll: { color: '#007AFF', fontSize: 14, fontWeight: '600' },
  memoriesRail: { flexDirection: 'row' },
  memoryItem: { width: 100, height: 100, backgroundColor: '#e0e0e0', borderRadius: 16, marginRight: 12, justifyContent: 'center', alignItems: 'center' },

  // MODAL
  modalOverlay: { flex: 1, backgroundColor: 'rgba(255,255,255,0.95)', justifyContent: 'flex-start', paddingTop: 60 },
  modalContent: { padding: 24, flex: 1 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 },
  modalTitle: { fontSize: 24, fontWeight: 'bold', color: '#333' },
  modalInputWrapper: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f0f2f5', borderRadius: 12, padding: 14 },
  modalInput: { flex: 1, fontSize: 16, marginLeft: 10, color: '#333' },
  resultItem: { flexDirection: 'row', alignItems: 'center', paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#eee' },
  resultIcon: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f0f0f0', justifyContent: 'center', alignItems: 'center', marginRight: 12 },
  resultTitle: { fontSize: 16, fontWeight: '600', color: '#333' },
  resultSubtitle: { fontSize: 13, color: '#666' },
});
