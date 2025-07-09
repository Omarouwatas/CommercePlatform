import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';
import axios from 'axios';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://192.168.0.110:5000/api/auth/login', {
        email,
        password,
      });
      setMsg('Connexion réussie');
    } catch (err) {
      setMsg(err.response?.data?.msg || 'Erreur');
    }
  };

  return (
    <View style={styles.container}>
      <Text variant="titleLarge">Connexion</Text>
      <TextInput label="Email" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput label="Mot de passe" value={password} onChangeText={setPassword} secureTextEntry style={styles.input} />
      <Button mode="contained" onPress={handleLogin}>Se connecter</Button>
      <Button onPress={() => navigation.navigate('Register')}>Créer un compte</Button>
      {msg ? <Text>{msg}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  input: { marginBottom: 10 },
});
