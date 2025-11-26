import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal, Animated } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const GDPRConsent = () => {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        checkConsent();
    }, []);

    const checkConsent = async () => {
        try {
            const consent = await AsyncStorage.getItem('gdpr_consent');
            if (!consent) {
                setVisible(true);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const handleAccept = async () => {
        try {
            await AsyncStorage.setItem('gdpr_consent', 'accepted');
            setVisible(false);
        } catch (e) {
            console.error(e);
        }
    };

    if (!visible) return null;

    return (
        <View style={styles.container}>
            <View style={styles.content}>
                <Text style={styles.title}>We value your privacy</Text>
                <Text style={styles.text}>
                    We use cookies and similar technologies to help personalize content, tailor and measure ads, and provide a better experience.
                    By clicking "Accept", you agree to this use of your data.
                </Text>
                <View style={styles.buttonRow}>
                    <TouchableOpacity style={styles.button} onPress={handleAccept}>
                        <Text style={styles.buttonText}>Accept</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'rgba(0,0,0,0.6)',
        zIndex: 1000,
        padding: 10,
    },
    content: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    title: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 8,
    },
    text: {
        fontSize: 14,
        color: '#666',
        marginBottom: 20,
        lineHeight: 20,
    },
    buttonRow: {
        flexDirection: 'row',
        justifyContent: 'flex-end',
    },
    button: {
        backgroundColor: '#007AFF',
        paddingVertical: 10,
        paddingHorizontal: 20,
        borderRadius: 8,
    },
    buttonText: {
        color: '#fff',
        fontWeight: '600',
        fontSize: 16,
    },
});

export default GDPRConsent;
