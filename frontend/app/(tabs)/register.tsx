import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';
import axios, { AxiosError } from 'axios';

import { useRouter } from 'expo-router';

export default function RegisterScreen() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [nom, setNom] = useState('');
  const [msg, setMsg] = useState('');

  const handleRegister = async () => {
    try {
      const res = await axios.post('http://<ton_ip>:5000/api/auth/register', {
        email,
        password,
        nom,
      });
      setMsg('Inscription réussie');
      router.replace('/login');
    } catch (err) {
        const error = err as AxiosError<any>;
      setMsg(error.response?.data?.msg || 'Erreur lors de l’inscription');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput label="Nom" value={nom} onChangeText={setNom} style={{ marginBottom: 10 }} />
      <TextInput label="Email" value={email} onChangeText={setEmail} style={{ marginBottom: 10 }} />
      <TextInput label="Mot de passe" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 10 }} />
      <Button mode="contained" onPress={handleRegister}>S’inscrire</Button>
      <Button onPress={() => router.replace('/login')}>Retour</Button>
      {msg ? <Text>{msg}</Text> : null}
    </View>
  );
}
