import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

const PrivacyScreen = () => {
  const router = useRouter();

  const openLink = (url: string) => {
    Linking.openURL(url);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Privacy Policy</Text>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={styles.scrollContent}>
        <Text style={styles.lastUpdated}>Last Updated: November 21, 2025</Text>

        <Text style={styles.sectionTitle}>1. Introduction</Text>
        <Text style={styles.paragraph}>
          Welcome to Trova. We respect your privacy and are committed to protecting your personal data.
          This privacy policy will inform you as to how we look after your personal data when you visit our app
          and tell you about your privacy rights and how the law protects you.
        </Text>

        <Text style={styles.sectionTitle}>2. Data We Collect</Text>
        <Text style={styles.paragraph}>
          We may collect, use, store and transfer different kinds of personal data about you which we have grouped together follows:
          {'\n'}• Identity Data: includes first name, last name, username.
          {'\n'}• Contact Data: includes email address.
          {'\n'}• Technical Data: includes internet protocol (IP) address, your login data, browser type and version.
          {'\n'}• Usage Data: includes information about how you use our app and services.
        </Text>

        <Text style={styles.sectionTitle}>3. How We Use Your Data</Text>
        <Text style={styles.paragraph}>
          We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:
          {'\n'}• Where we need to perform the contract we are about to enter into or have entered into with you.
          {'\n'}• Where it is necessary for our legitimate interests (or those of a third party) and your interests and fundamental rights do not override those interests.
          {'\n'}• Where we need to comply with a legal or regulatory obligation.
        </Text>

        <Text style={styles.sectionTitle}>4. Data Security</Text>
        <Text style={styles.paragraph}>
          We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed.
        </Text>

        <Text style={styles.sectionTitle}>5. Contact Us</Text>
        <Text style={styles.paragraph}>
          If you have any questions about this privacy policy or our privacy practices, please contact us at: support@trova.app
        </Text>

        <TouchableOpacity onPress={() => openLink('https://www.trova.app/privacy')} style={styles.linkButton}>
          <Text style={styles.linkText}>View Full Privacy Policy Online</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: { flexDirection: 'row', alignItems: 'center', padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee', marginTop: 40 },
  backButton: { padding: 8, marginRight: 8 },
  headerTitle: { fontSize: 20, fontWeight: 'bold' },
  content: { flex: 1 },
  scrollContent: { padding: 20, paddingBottom: 40 },
  lastUpdated: { fontSize: 14, color: '#666', marginBottom: 20, fontStyle: 'italic' },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10, color: '#333' },
  paragraph: { fontSize: 16, lineHeight: 24, color: '#444', marginBottom: 10 },
  linkButton: { marginTop: 30, padding: 15, backgroundColor: '#f0f0f0', borderRadius: 8, alignItems: 'center' },
  linkText: { color: '#007AFF', fontWeight: '600', fontSize: 16 },
});

export default PrivacyScreen;
