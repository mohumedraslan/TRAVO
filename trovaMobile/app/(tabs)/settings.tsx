import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Switch, ScrollView, Alert, Linking, Modal } from 'react-native';
import { useState } from 'react';

export default function SettingsScreen() {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [autoSync, setAutoSync] = useState(true);
  const [premiumActive, setPremiumActive] = useState(false);
  const [showPrivacy, setShowPrivacy] = useState(false);
  const [showTerms, setShowTerms] = useState(false);

  const handleUpgrade = () => {
    Alert.alert(
      'Upgrade to Premium',
      'Unlock unlimited AI scans, auto-reels, and group sharing!\n\n$4.99/month or $39.99/year',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Subscribe', onPress: () => setPremiumActive(true) }
      ]
    );
  };

  const handleExport = async () => {
    Alert.alert('Export Started', 'Your data will be exported and ready for download shortly.');
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>⚙️ Settings</Text>

      {/* Premium Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Subscription</Text>
        {premiumActive ? (
          <View style={styles.premiumBadge}>
            <Text style={styles.premiumText}>⭐ Premium Active</Text>
          </View>
        ) : (
          <TouchableOpacity style={styles.upgradeButton} onPress={handleUpgrade}>
            <Text style={styles.upgradeButtonText}>Upgrade to Premium</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Notifications */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Notifications</Text>
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Smart Notifications</Text>
          <Switch value={notificationsEnabled} onValueChange={setNotificationsEnabled} />
        </View>
        <Text style={styles.settingHint}>Get reminders to capture moments at landmarks</Text>
      </View>

      {/* Appearance */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Appearance</Text>
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Dark Mode</Text>
          <Switch value={darkMode} onValueChange={setDarkMode} />
        </View>
      </View>

      {/* Sync */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Data</Text>
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Auto Sync Photos</Text>
          <Switch value={autoSync} onValueChange={setAutoSync} />
        </View>
        <TouchableOpacity style={styles.exportButton} onPress={handleExport}>
          <Text style={styles.exportButtonText}>📤 Export All Data</Text>
        </TouchableOpacity>
      </View>

      {/* About */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <Text style={styles.aboutText}>TRAVO 2.0</Text>
        <Text style={styles.versionText}>Version 1.0.0</Text>
        <TouchableOpacity style={styles.linkButton} onPress={() => setShowPrivacy(true)}>
          <Text style={styles.linkText}>Privacy Policy</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.linkButton} onPress={() => setShowTerms(true)}>
          <Text style={styles.linkText}>Terms of Service</Text>
        </TouchableOpacity>
      </View>

      {/* Privacy Policy Modal */}
      <Modal visible={showPrivacy} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Privacy Policy</Text>
              <TouchableOpacity onPress={() => setShowPrivacy(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              <Text style={styles.legalText}>
                <Text style={styles.legalHeading}>Last Updated: December 2024{'\n\n'}</Text>

                <Text style={styles.legalHeading}>1. Information We Collect{'\n'}</Text>
                We collect photos you take, location data to tag your memories, and usage data to improve our service.{'\n\n'}

                <Text style={styles.legalHeading}>2. How We Use Your Data{'\n'}</Text>
                Your photos are analyzed by AI to identify landmarks. Photos are stored securely in cloud storage.{'\n\n'}

                <Text style={styles.legalHeading}>3. Data Storage{'\n'}</Text>
                Photos are stored in Supabase (EU servers). You can delete your data at any time.{'\n\n'}

                <Text style={styles.legalHeading}>4. Third Party Services{'\n'}</Text>
                We use Google Gemini for AI-powered image analysis. Your photos may be processed by Google.{'\n\n'}

                <Text style={styles.legalHeading}>5. Contact{'\n'}</Text>
                For questions, contact: support@travo.app
              </Text>
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Terms of Service Modal */}
      <Modal visible={showTerms} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Terms of Service</Text>
              <TouchableOpacity onPress={() => setShowTerms(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              <Text style={styles.legalText}>
                <Text style={styles.legalHeading}>Last Updated: December 2024{'\n\n'}</Text>

                <Text style={styles.legalHeading}>1. Acceptance of Terms{'\n'}</Text>
                By using TRAVO, you agree to these terms. If you do not agree, do not use the service.{'\n\n'}

                <Text style={styles.legalHeading}>2. Service Description{'\n'}</Text>
                TRAVO is a travel companion app that uses AI to identify landmarks in your photos.{'\n\n'}

                <Text style={styles.legalHeading}>3. User Responsibilities{'\n'}</Text>
                You are responsible for the photos you upload. Do not upload illegal or offensive content.{'\n\n'}

                <Text style={styles.legalHeading}>4. Premium Subscription{'\n'}</Text>
                Premium features require a subscription. Subscriptions auto-renew unless cancelled.{'\n\n'}

                <Text style={styles.legalHeading}>5. Limitation of Liability{'\n'}</Text>
                TRAVO is provided "as is". We are not liable for any damages arising from use of the app.{'\n\n'}

                <Text style={styles.legalHeading}>6. Contact{'\n'}</Text>
                For questions, contact: legal@travo.app
              </Text>
            </ScrollView>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 28, fontWeight: 'bold', marginBottom: 24, marginTop: 40 },
  section: { marginBottom: 28 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: '#333', marginBottom: 12 },
  settingRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8 },
  settingLabel: { fontSize: 16 },
  settingHint: { fontSize: 12, color: '#999', marginTop: 4 },
  premiumBadge: { backgroundColor: '#ffd700', borderRadius: 12, padding: 16, alignItems: 'center' },
  premiumText: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  upgradeButton: { backgroundColor: '#6200ea', borderRadius: 12, padding: 16, alignItems: 'center' },
  upgradeButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  exportButton: { backgroundColor: '#f5f5f5', borderRadius: 8, padding: 12, marginTop: 12, alignItems: 'center' },
  exportButtonText: { fontSize: 14, color: '#333' },
  aboutText: { fontSize: 18, fontWeight: '600' },
  versionText: { fontSize: 14, color: '#666', marginTop: 4 },
  linkButton: { paddingVertical: 12 },
  linkText: { color: '#1976d2', fontSize: 16 },
  // Modal styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: '#fff', borderTopLeftRadius: 20, borderTopRightRadius: 20, maxHeight: '80%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 20, borderBottomWidth: 1, borderBottomColor: '#eee' },
  modalTitle: { fontSize: 20, fontWeight: 'bold' },
  closeButton: { fontSize: 24, color: '#666' },
  modalScroll: { padding: 20 },
  legalText: { fontSize: 14, lineHeight: 22, color: '#333' },
  legalHeading: { fontWeight: 'bold', fontSize: 15 },
});
