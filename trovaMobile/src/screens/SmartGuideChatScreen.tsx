import React from 'react';
import { View, StyleSheet, SafeAreaView } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import SmartGuideChat from '@/src/components/SmartGuideChat';

const SmartGuideChatScreen: React.FC = () => {
  const { location } = useLocalSearchParams<{ location: string }>();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.chatContainer}>
        <SmartGuideChat initialLocation={location} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  chatContainer: {
    flex: 1,
  },
});

export default SmartGuideChatScreen;