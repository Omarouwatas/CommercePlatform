import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';
import axios from 'axios';

export default function RegisterScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [nom, setNom] = useState('');
  const [msg, setMsg] = useState('');

  const handleRegister = async () => {
    try {
      const res = await axios.post('http://192.168.0.110:5000/api/auth/register', {
        email,
        password,
        nom,
      });
      setMsg('Compte créé avec succès');
    } catch (err) {
      setMsg(err.response?.data?.msg || 'Erreur');
    }
  };

  return (
    <View style={styles.container}>
      <Text variant="titleLarge">Créer un compte</Text>
      <TextInput label="Nom" value={nom} onChangeText={setNom} style={styles.input} />
      <TextInput label="Email" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput label="Mot de passe" value={password} onChangeText={setPassword} secureTextEntry style={styles.input} />
      <Button mode="contained" onPress={handleRegister}>S’inscrire</Button>
      <Button onPress={() => navigation.goBack()}>Retour</Button>
      {msg ? <Text>{msg}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  input: { marginBottom: 10 },
});
