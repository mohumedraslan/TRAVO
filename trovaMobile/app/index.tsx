import { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { useRouter, Slot } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Index() {
    const router = useRouter();
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            // Check for explicit "Guest" flag or "User Token"
            const isGuest = await AsyncStorage.getItem('isGuest');
            const userToken = await AsyncStorage.getItem('userToken');

            if (isGuest === 'true' || userToken) {
                // User is allowed
                router.replace('/(tabs)');
            } else {
                // No access yet
                router.replace('/login');
            }
        } catch (e) {
            // Fallback (e.g. storage error)
            router.replace('/login');
        } finally {
            setChecking(false);
        }
    };

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <ActivityIndicator size="large" color="#007AFF" />
        </View>
    );
}
