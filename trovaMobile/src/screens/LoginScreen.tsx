import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

interface Props {
  navigation: any;
}

const LoginScreen: React.FC<Props> = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      // TODO: replace with real backend endpoint
      const res = await axios.post('http://localhost:8000/api/auth/login', {
        email,
        password,
      });
      Alert.alert('Logged in', `Welcome ${res.data?.user?.name || email}`);
      navigation.replace('Explore');
    } catch (err: any) {
      Alert.alert('Login failed', err?.response?.data?.message || 'Please try again');
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 24 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 24, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, marginBottom: 12 },
});

export default LoginScreen;
