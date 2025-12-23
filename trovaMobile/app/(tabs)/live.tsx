import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as ImageManipulator from 'expo-image-manipulator';
import * as Location from 'expo-location';
import { useIsFocused } from '@react-navigation/native';
import client from '../../src/api/client';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function LiveScreen() {
    const [permission, requestPermission] = useCameraPermissions();
    const [isDataActive, setIsDataActive] = useState(false);
    const [lastTip, setLastTip] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const cameraRef = useRef<CameraView>(null);
    const isFocused = useIsFocused();
    const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

    // UX: Rotating "Thinking" messages
    const [thinkingMessage, setThinkingMessage] = useState("Analyzing...");
    const thinkingIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    const THINKING_MESSAGES = [
        "Scanning scene... 📷",
        "Reading coordinates... 📍",
        "identifying landmarks... 🏛️",
        "Checking travel guide... 📚",
        "Polishing answer... ✨",
        "Almost there... 🚀"
    ];

    // Initial Permissions
    useEffect(() => {
        if (!permission?.granted) {
            requestPermission();
        }
    }, [permission]);

    // Main Pulse Loop
    useEffect(() => {
        if (isFocused && isDataActive) {
            startPulse();
        } else {
            stopPulse();
        }
        return () => stopPulse();
    }, [isFocused, isDataActive]);

    const startPulse = () => {
        // Immediate first pulse
        sendPulse();
        // Then every 10 seconds
        timerRef.current = setInterval(sendPulse, 10000);
    };

    const stopPulse = () => {
        if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
        }
    };

    const sendPulse = async () => {
        if (!cameraRef.current || loading) return;

        try {
            setLoading(true);

            // Start Thinking Animation
            let msgIndex = 0;
            setThinkingMessage(THINKING_MESSAGES[0]);
            thinkingIntervalRef.current = setInterval(() => {
                msgIndex = (msgIndex + 1) % THINKING_MESSAGES.length;
                setThinkingMessage(THINKING_MESSAGES[msgIndex]);
            }, 2500);

            // 1. Take Snapshot
            const photo = await cameraRef.current.takePictureAsync({
                quality: 0.5,
                skipProcessing: true, // Fast!
            });

            if (!photo) return;

            // 2. Resize (Crucial for bandwidth/speed)
            const manipResult = await ImageManipulator.manipulateAsync(
                photo.uri,
                [{ resize: { width: 512 } }], // 512px width is plenty for context
                { compress: 0.7, format: ImageManipulator.SaveFormat.JPEG }
            );

            // 3. Get Location
            let lat = 0, lon = 0;
            try {
                const { status } = await Location.requestForegroundPermissionsAsync();
                if (status === 'granted') {
                    const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
                    lat = loc.coords.latitude;
                    lon = loc.coords.longitude;
                }
            } catch (e) { /* ignore location errors */ }

            // 4. Send to API
            const formData = new FormData();
            formData.append('image', {
                uri: manipResult.uri,
                type: 'image/jpeg',
                name: 'pulse.jpg',
            } as any);
            if (lat) formData.append('lat', String(lat));
            if (lon) formData.append('lon', String(lon));

            const res = await client.post('/live/pulse', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                timeout: 30000, // 30s for Local AI (can be slow to load first time)
            });

            setLastTip(res.data.tip);

        } catch (err) {
            console.log('Pulse skipped/failed:', err);
        } finally {
            setLoading(false);
            if (thinkingIntervalRef.current) clearInterval(thinkingIntervalRef.current);
        }
    };

    if (!permission) return <View />;
    if (!permission.granted) {
        return (
            <View style={styles.container}>
                <Text style={{ textAlign: 'center', marginTop: 50 }}>Camera permission required</Text>
                <TouchableOpacity onPress={requestPermission} style={styles.permButton}>
                    <Text style={{ color: 'white' }}>Grant Permission</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {isFocused && (
                <CameraView
                    style={styles.camera}
                    facing="back"
                    ref={cameraRef}
                >
                    {/* Overlay UI */}
                    <View style={styles.overlay}>

                        {/* Top Bar: Status */}
                        <View style={styles.topBar}>
                            <View style={[styles.statusBadge, isDataActive ? styles.activeBadge : styles.inactiveBadge]}>
                                <View style={[styles.dot, isDataActive && styles.pulsingDot]} />
                                <Text style={styles.statusText}>{isDataActive ? 'LIVE ANALYSIS ON' : 'PAUSED'}</Text>
                            </View>
                        </View>

                        {/* Middle: Tip Bubble */}
                        {lastTip && isDataActive && (
                            <View style={styles.tipContainer}>
                                <View style={styles.tipBubble}>
                                    <Text style={styles.tipIcon}>🤖</Text>
                                    <Text style={styles.tipText}>{lastTip}</Text>
                                </View>
                            </View>
                        )}

                        {/* Bottom: Controls */}
                        <View style={styles.bottomBar}>
                            <TouchableOpacity
                                style={[styles.toggleButton, isDataActive ? styles.stopButton : styles.startButton]}
                                onPress={() => setIsDataActive(!isDataActive)}
                            >
                                <IconSymbol
                                    size={32}
                                    name={isDataActive ? "stop.fill" : "play.fill"}
                                    color="white"
                                />
                                <Text style={styles.buttonText}>
                                    {isDataActive ? "Stop Analysis" : "Start Live Mode"}
                                </Text>
                            </TouchableOpacity>

                            {loading && (
                                <View style={styles.thinkingContainer}>
                                    <ActivityIndicator size="small" color="#FFF" />
                                    <Text style={styles.thinkingText}>{thinkingMessage}</Text>
                                </View>
                            )}
                        </View>

                    </View>
                </CameraView>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: 'black' },
    camera: { flex: 1 },
    overlay: { flex: 1, justifyContent: 'space-between', padding: 20, paddingTop: 60 },
    topBar: { alignItems: 'center' },
    statusBadge: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, borderWidth: 1 },
    activeBadge: { backgroundColor: 'rgba(52, 199, 89, 0.2)', borderColor: '#34C759' },
    inactiveBadge: { backgroundColor: 'rgba(0, 0, 0, 0.5)', borderColor: '#666' },
    dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#666', marginRight: 8 },
    pulsingDot: { backgroundColor: '#34C759' },
    statusText: { color: 'white', fontWeight: 'bold', fontSize: 12, letterSpacing: 1 },

    tipContainer: { alignItems: 'center', marginHorizontal: 20 },
    tipBubble: { flexDirection: 'row', backgroundColor: 'rgba(255, 255, 255, 0.95)', padding: 16, borderRadius: 16, maxWidth: '100%', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.25, shadowRadius: 3.84, elevation: 5 },
    tipIcon: { fontSize: 24, marginRight: 12 },
    tipText: { flex: 1, fontSize: 16, color: '#333', lineHeight: 22, fontWeight: '500' },

    bottomBar: { alignItems: 'center', marginBottom: 30 },
    toggleButton: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 32, paddingVertical: 16, borderRadius: 30, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 4.65, elevation: 8 },
    startButton: { backgroundColor: '#007AFF' },
    stopButton: { backgroundColor: '#FF3B30' },
    buttonText: { color: 'white', fontSize: 18, fontWeight: 'bold', marginLeft: 10 },
    permButton: { backgroundColor: '#007AFF', padding: 15, borderRadius: 10, marginTop: 20 },

    thinkingContainer: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.6)', paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, marginTop: 12 },
    thinkingText: { color: 'white', marginLeft: 8, fontSize: 14, fontWeight: '600' },
});
