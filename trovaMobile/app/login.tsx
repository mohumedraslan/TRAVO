import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, Image, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import client from '../src/api/client'; // Corrected path

export default function LoginScreen() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        if (!email || !password) {
            Alert.alert("Missing Fields", "Please enter email and password.");
            return;
        }

        setLoading(true);
        try {
            // Attempt Login
            // Note: Update URL if your backend uses a specific Auth path
            const res = await client.post('/auth/login', { email, password });

            // Save Token (Mock or Real)
            await AsyncStorage.setItem('userToken', res.data.token || 'mock-token');
            await AsyncStorage.setItem('userId', res.data.user?.id || 'user-123');

            router.replace('/(tabs)');
        } catch (err: any) {
            console.log("Login Error:", err);
            Alert.alert("Login Failed", "Invalid credentials or server error. Try Guest Mode!");
        } finally {
            setLoading(false);
        }
    };

    const handleGuest = async () => {
        setLoading(true);
        // Set Guest Flag
        await AsyncStorage.setItem('isGuest', 'true');
        await AsyncStorage.setItem('userId', 'anonymous');

        // Small delay for UX
        setTimeout(() => {
            setLoading(false);
            router.replace('/(tabs)');
        }, 500);
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.logo}>🌍 TRAVO</Text>
                <Text style={styles.subtitle}>Your AI Travel Companion</Text>
            </View>

            <View style={styles.form}>
                <TextInput
                    style={styles.input}
                    placeholder="Email"
                    value={email}
                    onChangeText={setEmail}
                    autoCapitalize="none"
                    keyboardType="email-address"
                    placeholderTextColor="#999"
                />
                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry
                    placeholderTextColor="#999"
                />

                <TouchableOpacity style={styles.loginButton} onPress={handleLogin} disabled={loading}>
                    {loading ? <ActivityIndicator color="white" /> : <Text style={styles.loginText}>Log In</Text>}
                </TouchableOpacity>

                <View style={styles.divider}>
                    <View style={styles.line} />
                    <Text style={styles.orText}>OR</Text>
                    <View style={styles.line} />
                </View>

                {/* GUEST BUTTON */}
                <TouchableOpacity style={styles.guestButton} onPress={handleGuest} disabled={loading}>
                    <Text style={styles.guestText}>Continue as Guest 🕶️</Text>
                </TouchableOpacity>
                <Text style={styles.guestHint}>No account? No problem. Features are unlocked.</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff', padding: 24, justifyContent: 'center' },
    header: { alignItems: 'center', marginBottom: 48 },
    logo: { fontSize: 42, fontWeight: '900', color: '#007AFF', marginBottom: 8 },
    subtitle: { fontSize: 18, color: '#666' },
    form: { width: '100%' },
    input: { backgroundColor: '#f0f2f5', padding: 16, borderRadius: 12, marginBottom: 16, fontSize: 16 },
    loginButton: { backgroundColor: '#007AFF', padding: 16, borderRadius: 12, alignItems: 'center', marginBottom: 24 },
    loginText: { color: 'white', fontSize: 16, fontWeight: 'bold' },
    divider: { flexDirection: 'row', alignItems: 'center', marginBottom: 24 },
    line: { flex: 1, height: 1, backgroundColor: '#eee' },
    orText: { marginHorizontal: 16, color: '#999', fontWeight: '600' },
    guestButton: { backgroundColor: '#34C759', padding: 16, borderRadius: 12, alignItems: 'center' },
    guestText: { color: 'white', fontSize: 16, fontWeight: 'bold' },
    guestHint: { textAlign: 'center', marginTop: 12, color: '#999', fontSize: 13 },
});
