import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, Modal, FlatList, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import client from '../../src/api/client';

interface SearchResult {
  id: string;
  type: string;
  title: string;
  subtitle: string;
}

export default function HomeScreen() {
  const router = useRouter();
  const [searchVisible, setSearchVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);

  const quickActions = [
    { icon: '📷', label: 'Capture', route: '/camera' },
    { icon: '✈️', label: 'Start Trip', route: '/trip' },
    { icon: '📖', label: 'Daily Story', route: '/daily' },
    { icon: '🗺️', label: 'World Map', route: '/map' },
  ];

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      // Mock results - would call /assistant/query
      setSearchResults([
        { id: '1', type: 'photo', title: 'Coffee at Nile Cafe', subtitle: 'Dec 5, Cairo' },
        { id: '2', type: 'trip', title: 'Egypt Adventure', subtitle: '24 photos' },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setSearching(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      {/* Header with Search */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <Text style={styles.greeting}>Welcome back! 👋</Text>
          <TouchableOpacity style={styles.searchIcon} onPress={() => setSearchVisible(true)}>
            <Text style={styles.searchIconText}>🔍</Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.subtitle}>Ready to capture memories?</Text>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        {quickActions.map((action, i) => (
          <TouchableOpacity
            key={i}
            style={styles.actionCard}
            onPress={() => router.push(action.route as any)}
          >
            <Text style={styles.actionIcon}>{action.icon}</Text>
            <Text style={styles.actionLabel}>{action.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Active Trip */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Active Trip</Text>
        <TouchableOpacity style={styles.tripCard} onPress={() => router.push('/trip')}>
          <Text style={styles.tripName}>🌍 Egypt Adventure</Text>
          <Text style={styles.tripStats}>Day 5 • 24 photos</Text>
        </TouchableOpacity>
      </View>

      {/* Recent Photos */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Photos</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {[1, 2, 3].map((_, i) => (
            <View key={i} style={styles.photoCard}>
              <Text style={styles.photoIcon}>🏛️</Text>
            </View>
          ))}
        </ScrollView>
      </View>

      {/* Search Modal */}
      <Modal visible={searchVisible} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>🔍 AI Search</Text>
              <TouchableOpacity onPress={() => setSearchVisible(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>
            <TextInput
              style={styles.searchInput}
              placeholder="Where did I have coffee last week?"
              value={searchQuery}
              onChangeText={setSearchQuery}
              onSubmitEditing={handleSearch}
              returnKeyType="search"
              autoFocus
            />
            {searching && <ActivityIndicator style={{ marginTop: 20 }} />}
            <FlatList
              data={searchResults}
              keyExtractor={(item) => item.id}
              renderItem={({ item }) => (
                <TouchableOpacity style={styles.resultItem}>
                  <Text style={styles.resultTitle}>{item.title}</Text>
                  <Text style={styles.resultSubtitle}>{item.subtitle}</Text>
                </TouchableOpacity>
              )}
            />
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: { padding: 20, paddingTop: 60, backgroundColor: '#1976d2' },
  headerTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  greeting: { fontSize: 28, fontWeight: 'bold', color: '#fff' },
  searchIcon: { backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: 20, padding: 10 },
  searchIconText: { fontSize: 20 },
  subtitle: { fontSize: 16, color: '#fff', opacity: 0.9, marginTop: 4 },
  quickActions: { flexDirection: 'row', padding: 16, gap: 12 },
  actionCard: { flex: 1, backgroundColor: '#f5f5f5', borderRadius: 16, padding: 16, alignItems: 'center' },
  actionIcon: { fontSize: 28 },
  actionLabel: { fontSize: 11, fontWeight: '600', marginTop: 6, color: '#333' },
  section: { padding: 16 },
  sectionTitle: { fontSize: 18, fontWeight: '600', marginBottom: 12 },
  tripCard: { backgroundColor: '#e8f5e9', borderRadius: 16, padding: 16 },
  tripName: { fontSize: 18, fontWeight: '600' },
  tripStats: { fontSize: 14, color: '#666', marginTop: 4 },
  photoCard: { width: 100, height: 100, backgroundColor: '#e0e0e0', borderRadius: 12, marginRight: 12, justifyContent: 'center', alignItems: 'center' },
  photoIcon: { fontSize: 32 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: '#fff', borderTopLeftRadius: 20, borderTopRightRadius: 20, padding: 20, minHeight: 400 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  modalTitle: { fontSize: 20, fontWeight: 'bold' },
  closeButton: { fontSize: 24, color: '#666' },
  searchInput: { backgroundColor: '#f5f5f5', borderRadius: 12, padding: 14, fontSize: 16 },
  resultItem: { paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#eee' },
  resultTitle: { fontSize: 16, fontWeight: '600' },
  resultSubtitle: { fontSize: 13, color: '#666', marginTop: 2 },
});
