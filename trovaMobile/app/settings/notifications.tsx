import { View, Text, StyleSheet } from 'react-native';

export default function NotificationsScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Notifications Settings</Text>
            <Text style={styles.subtext}>Coming soon...</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
    text: { fontSize: 20, fontWeight: 'bold' },
    subtext: { fontSize: 16, color: '#666', marginTop: 8 },
});
