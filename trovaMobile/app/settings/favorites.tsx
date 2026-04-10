import { View, Text, StyleSheet } from 'react-native';

export default function FavoritesScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Your Favorites</Text>
            <Text style={styles.subtext}>No favorites yet.</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
    text: { fontSize: 20, fontWeight: 'bold' },
    subtext: { fontSize: 16, color: '#666', marginTop: 8 },
});
