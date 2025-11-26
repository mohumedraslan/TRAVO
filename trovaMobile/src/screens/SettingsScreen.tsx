import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Switch, Linking, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { supabase } from '../config/supabase';

const SettingsScreen = () => {
  const router = useRouter();
  const [profile, setProfile] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(false);
  const [notifications, setNotifications] = React.useState(true);
  const [darkMode, setDarkMode] = React.useState(false);

  React.useEffect(() => {
    fetchProfile();
  }, []);

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) Alert.alert('Error', error.message);
    else router.replace('/login');
  };

  const handleHelp = () => {
    Linking.openURL('mailto:support@trova.app');
  };

  const toggleDarkMode = (value: boolean) => {
    setDarkMode(value);
    // In a real app, this would update a global theme context
    Alert.alert('Theme', `Dark mode ${value ? 'enabled' : 'disabled'} (UI update requires restart or context)`);
  };

  const fetchProfile = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', user.id)
          .single();

        if (error) throw error;
        setProfile(data);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const updateProfile = async (key: string, value: any) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      const { error } = await supabase
        .from('profiles')
        .update({ [key]: value })
        .eq('id', user.id);

      if (error) throw error;
      setProfile({ ...profile, [key]: value });
    } catch (error: any) {
      Alert.alert('Error updating profile', error.message);
    }
  };

  return (
    <ScrollView style={[styles.container, darkMode && styles.darkContainer]}>
      <View style={[styles.section, darkMode && styles.darkSection]}>
        <Text style={[styles.sectionTitle, darkMode && styles.darkText]}>Profile</Text>
        {profile && (
          <>
            <View style={[styles.row, darkMode && styles.darkRow]}>
              <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Name</Text>
              <Text style={[styles.valueText, darkMode && styles.darkText]}>{profile.full_name}</Text>
            </View>
            <View style={[styles.row, darkMode && styles.darkRow]}>
              <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Username</Text>
              <Text style={[styles.valueText, darkMode && styles.darkText]}>{profile.username}</Text>
            </View>
          </>
        )}
      </View>

      <View style={[styles.section, darkMode && styles.darkSection]}>
        <Text style={[styles.sectionTitle, darkMode && styles.darkText]}>Preferences</Text>

        <View style={[styles.row, darkMode && styles.darkRow]}>
          <View style={styles.rowLeft}>
            <Ionicons name="notifications-outline" size={22} color={darkMode ? "#fff" : "#333"} />
            <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Notifications</Text>
          </View>
          <Switch value={notifications} onValueChange={setNotifications} />
        </View>

        <View style={[styles.row, darkMode && styles.darkRow]}>
          <View style={styles.rowLeft}>
            <Ionicons name="moon-outline" size={22} color={darkMode ? "#fff" : "#333"} />
            <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Dark Mode</Text>
          </View>
          <Switch value={darkMode} onValueChange={toggleDarkMode} />
        </View>

        {profile && (
          <>
            <TouchableOpacity style={[styles.row, darkMode && styles.darkRow]} onPress={() => {
              Alert.prompt('Update Language', 'Enter your preferred language code (e.g. en, es)', [
                { text: 'Cancel', style: 'cancel' },
                { text: 'Save', onPress: (val: string | undefined) => updateProfile('language', val) }
              ], 'plain-text', profile.language);
            }}>
              <View style={styles.rowLeft}>
                <Ionicons name="language-outline" size={22} color={darkMode ? "#fff" : "#333"} />
                <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Language</Text>
              </View>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <Text style={{ color: '#999', marginRight: 10 }}>{profile.language}</Text>
                <Ionicons name="chevron-forward" size={20} color="#ccc" />
              </View>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.row, darkMode && styles.darkRow]} onPress={() => {
              Alert.prompt('Update Interests', 'Enter interests separated by commas', [
                { text: 'Cancel', style: 'cancel' },
                { text: 'Save', onPress: (val: string | undefined) => updateProfile('interests', val?.split(',').map((s: string) => s.trim()).filter(Boolean)) }
              ], 'plain-text', profile.interests?.join(', '));
            }}>
              <View style={styles.rowLeft}>
                <Ionicons name="heart-outline" size={22} color={darkMode ? "#fff" : "#333"} />
                <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Interests</Text>
              </View>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <Text style={{ color: '#999', marginRight: 10, maxWidth: 100 }} numberOfLines={1}>{profile.interests?.join(', ')}</Text>
                <Ionicons name="chevron-forward" size={20} color="#ccc" />
              </View>
            </TouchableOpacity>
          </>
        )}
      </View>

      <View style={[styles.section, darkMode && styles.darkSection]}>
        <Text style={[styles.sectionTitle, darkMode && styles.darkText]}>Support & Legal</Text>

        <TouchableOpacity style={[styles.row, darkMode && styles.darkRow]} onPress={handleHelp}>
          <View style={styles.rowLeft}>
            <Ionicons name="help-circle-outline" size={22} color={darkMode ? "#fff" : "#333"} />
            <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Help & Support</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity style={[styles.row, darkMode && styles.darkRow]} onPress={() => router.push('/privacy')}>
          <View style={styles.rowLeft}>
            <Ionicons name="lock-closed-outline" size={22} color={darkMode ? "#fff" : "#333"} />
            <Text style={[styles.rowLabel, darkMode && styles.darkText]}>Privacy Policy</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#ccc" />
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={[styles.logoutButton, darkMode && styles.darkButton]} onPress={handleLogout}>
        <Text style={styles.logoutText}>Log Out</Text>
      </TouchableOpacity>

      <Text style={styles.version}>Version 1.0.0</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  darkContainer: { backgroundColor: '#121212' },
  section: { marginTop: 20, backgroundColor: '#fff', borderTopWidth: 1, borderBottomWidth: 1, borderColor: '#eee' },
  darkSection: { backgroundColor: '#1e1e1e', borderColor: '#333' },
  sectionTitle: { fontSize: 14, fontWeight: '600', color: '#666', padding: 16, paddingBottom: 8, backgroundColor: '#f5f5f5' },
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  darkRow: { borderBottomColor: '#333' },
  rowLeft: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  rowLabel: { fontSize: 16, color: '#333' },
  darkText: { color: '#fff' },
  logoutButton: { marginTop: 40, marginHorizontal: 20, padding: 16, backgroundColor: '#fff', borderRadius: 8, alignItems: 'center', borderWidth: 1, borderColor: '#ff3b30' },
  darkButton: { backgroundColor: '#1e1e1e', borderColor: '#ff3b30' },
  logoutText: { color: '#ff3b30', fontSize: 16, fontWeight: '600' },
  valueText: { fontSize: 16, color: '#666' },
  version: { textAlign: 'center', marginTop: 20, color: '#999', fontSize: 12, marginBottom: 40 },
});

export default SettingsScreen;
