import React, { useState } from 'react';
import { View, TextInput, Button } from 'react-native';
import api from '../services/api';
import { generatePassword } from '../components/Generator';
import { colors } from '../theme/colors';

export default function EditPasswordScreen({ route, navigation }: any) {
  const item = route.params?.item;
  const [site, setSite] = useState(item?.site || '');
  const [username, setUsername] = useState(item?.username || '');
  const [password, setPassword] = useState(item?.password || '');
  const [notes, setNotes] = useState(item?.notes || '');

  const save = async () => {
    const payload = { site, username, password, notes, tags: [] };
    if (item?.id) await api.put(`/vault/${item.id}`, payload);
    else await api.post('/vault', payload);
    navigation.goBack();
  };

  return <View style={{ flex: 1, backgroundColor: colors.bg, padding: 16, gap: 10 }}>
    <TextInput placeholder="Site" placeholderTextColor="#999" value={site} onChangeText={setSite} style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} />
    <TextInput placeholder="Username" placeholderTextColor="#999" value={username} onChangeText={setUsername} style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} />
    <TextInput placeholder="Password" placeholderTextColor="#999" value={password} onChangeText={setPassword} style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} />
    <TextInput placeholder="Notes" placeholderTextColor="#999" value={notes} onChangeText={setNotes} style={{ color: colors.text, borderBottomWidth: 1, borderColor: '#555' }} />
    <Button title="Generate Password" onPress={() => setPassword(generatePassword())} />
    <Button title="Save" onPress={save} />
  </View>;
}
