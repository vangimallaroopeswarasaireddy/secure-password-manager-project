import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { useAuth } from '../hooks/useAuth';
import { colors } from '../theme/colors';

export default function LoginScreen({ navigation }: any) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View style={{ flex: 1, backgroundColor: colors.bg, padding: 20, gap: 10 }}>
      <Text style={{ color: colors.text, fontSize: 24 }}>Login</Text>
      <TextInput placeholder="Email" placeholderTextColor="#aaa" style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput placeholder="Master Password" secureTextEntry placeholderTextColor="#aaa" style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} onChangeText={setPassword} />
      <Button title="Login" onPress={async () => { try { await login(email, password); } catch { Alert.alert('Login failed'); } }} />
      <Button title="Create account" onPress={() => navigation.navigate('Register')} />
    </View>
  );
}
