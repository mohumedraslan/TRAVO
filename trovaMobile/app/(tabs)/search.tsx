import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, FlatList, ActivityIndicator } from 'react-native';
import client from '../../src/api/client';

interface SearchResult {
    id: string;
    type: 'photo' | 'trip' | 'location';
    title: string;
    subtitle: string;
    date: string;
}

export default function SearchScreen() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setLoading(true);
        setSearched(true);

        try {
            // Call AI assistant for natural language search
            const response = await client.post('/assistant/query', {
                question: query,
                context: 'travel_search'
            });

            // Mock results for now
            const mockResults: SearchResult[] = [
                { id: '1', type: 'photo', title: 'Coffee at Nile View Cafe', subtitle: 'Cairo, Egypt', date: 'Dec 5, 2024' },
                { id: '2', type: 'location', title: 'Khan el-Khalili', subtitle: 'Historic bazaar', date: 'Dec 4, 2024' },
                { id: '3', type: 'trip', title: 'Egypt Adventure', subtitle: '24 photos', date: 'Dec 1-8, 2024' },
            ];

            setResults(mockResults);
        } catch (err) {
            console.error('Search error:', err);
            // Use mock data on error
            setResults([
                { id: '1', type: 'photo', title: 'Example Photo', subtitle: 'No connection to server', date: 'Today' }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'photo': return '📷';
            case 'trip': return '✈️';
            case 'location': return '📍';
            default: return '🔍';
        }
    };

    const renderResult = ({ item }: { item: SearchResult }) => (
        <TouchableOpacity style={styles.resultCard}>
            <Text style={styles.resultIcon}>{getTypeIcon(item.type)}</Text>
            <View style={styles.resultInfo}>
                <Text style={styles.resultTitle}>{item.title}</Text>
                <Text style={styles.resultSubtitle}>{item.subtitle}</Text>
            </View>
            <Text style={styles.resultDate}>{item.date}</Text>
        </TouchableOpacity>
    );

    const exampleQueries = [
        "Where did I have coffee last week?",
        "Show me photos from Egypt",
        "When was I at the Pyramids?",
        "Find my sunset photos"
    ];

    return (
        <View style={styles.container}>
            <Text style={styles.title}>🔍 AI Search</Text>
            <Text style={styles.subtitle}>Ask anything about your travels</Text>

            <View style={styles.searchBox}>
                <TextInput
                    style={styles.input}
                    placeholder="e.g., Where did I have coffee last week?"
                    value={query}
                    onChangeText={setQuery}
                    onSubmitEditing={handleSearch}
                    returnKeyType="search"
                />
                <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
                    <Text style={styles.searchButtonText}>Search</Text>
                </TouchableOpacity>
            </View>

            {!searched && (
                <View style={styles.suggestions}>
                    <Text style={styles.suggestionsTitle}>Try asking:</Text>
                    {exampleQueries.map((q, i) => (
                        <TouchableOpacity key={i} style={styles.suggestionChip} onPress={() => setQuery(q)}>
                            <Text style={styles.suggestionText}>{q}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            )}

            {loading && <ActivityIndicator size="large" color="#007AFF" style={{ marginTop: 40 }} />}

            {searched && !loading && (
                <FlatList
                    data={results}
                    renderItem={renderResult}
                    keyExtractor={(item) => item.id}
                    ListEmptyComponent={<Text style={styles.noResults}>No results found</Text>}
                    contentContainerStyle={{ paddingBottom: 100 }}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff', padding: 16 },
    title: { fontSize: 28, fontWeight: 'bold' },
    subtitle: { fontSize: 14, color: '#666', marginBottom: 20 },
    searchBox: { flexDirection: 'row', marginBottom: 20 },
    input: { flex: 1, backgroundColor: '#f5f5f5', borderRadius: 12, padding: 14, fontSize: 16 },
    searchButton: { backgroundColor: '#007AFF', borderRadius: 12, paddingHorizontal: 20, justifyContent: 'center', marginLeft: 10 },
    searchButtonText: { color: '#fff', fontWeight: '600' },
    suggestions: { marginBottom: 20 },
    suggestionsTitle: { fontSize: 14, color: '#666', marginBottom: 12 },
    suggestionChip: { backgroundColor: '#e3f2fd', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 10, marginBottom: 8 },
    suggestionText: { color: '#1976d2', fontSize: 14 },
    resultCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f9f9f9', borderRadius: 12, padding: 14, marginBottom: 10 },
    resultIcon: { fontSize: 24, marginRight: 12 },
    resultInfo: { flex: 1 },
    resultTitle: { fontSize: 16, fontWeight: '600' },
    resultSubtitle: { fontSize: 13, color: '#666', marginTop: 2 },
    resultDate: { fontSize: 12, color: '#999' },
    noResults: { textAlign: 'center', color: '#999', marginTop: 40 },
});
