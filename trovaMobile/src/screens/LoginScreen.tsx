import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import client from '../api/client';

interface Props {
  navigation: any;
}

const LoginScreen: React.FC<Props> = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      // Use correct backend endpoint with OAuth2PasswordRequestForm fields
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);
      const res = await client.post('/user/login', form.toString(), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      Alert.alert('Logged in', `Welcome ${res.data?.user?.name || email}`);
      navigation.replace('Explore');
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Please try again';
      Alert.alert('Login failed', msg);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to Trova</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Login" onPress={handleLogin} />
      <View style={{ height: 16 }} />
      <Button title="Go to Explore" onPress={() => navigation.navigate('Explore')} />
      <View style={styles.signupContainer}>
        <Text>Don't have an account? </Text>
        <Text style={styles.link} onPress={() => navigation.navigate('Signup')}>
          Sign Up
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 24 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 24, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, marginBottom: 12 },
  signupContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 24,
  },
  link: {
    color: '#007AFF',
    fontWeight: '600',
  },
});

export default LoginScreen;
