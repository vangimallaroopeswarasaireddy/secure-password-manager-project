import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { useAuth } from '../hooks/useAuth';
import PasswordStrengthMeter from '../components/PasswordStrengthMeter';
import { colors } from '../theme/colors';

export default function RegisterScreen({ navigation }: any) {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return <View style={{ flex: 1, backgroundColor: colors.bg, padding: 20, gap: 10 }}>
    <Text style={{ color: colors.text, fontSize: 24 }}>Register</Text>
    <TextInput placeholder="Email" placeholderTextColor="#aaa" style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} onChangeText={setEmail} autoCapitalize="none" />
    <TextInput placeholder="Master Password" secureTextEntry placeholderTextColor="#aaa" style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} onChangeText={setPassword} />
    <PasswordStrengthMeter password={password} />
    <Button title="Register" onPress={async () => { try { await register(email, password); navigation.goBack(); } catch { Alert.alert('Registration failed'); } }} />
  </View>;
}
