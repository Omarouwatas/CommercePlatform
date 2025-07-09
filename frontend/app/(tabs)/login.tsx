import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';
import { useRouter } from 'expo-router';
import axios, { AxiosError } from 'axios';

export default function LoginScreen() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://<ton_ip>:5000/api/auth/login', { email, password });
      setMsg('Connexion réussie');
    } catch (err) {
      const error = err as AxiosError<any>;
      setMsg(error.response?.data?.msg || 'Erreur');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput label="Email" value={email} onChangeText={setEmail} style={{ marginBottom: 10 }} />
      <TextInput label="Mot de passe" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 10 }} />
      <Button mode="contained" onPress={handleLogin}>Connexion</Button>
      <Button onPress={() => router.push('/register')}>Créer un compte</Button>
      {msg ? <Text>{msg}</Text> : null}
    </View>
  );
}
