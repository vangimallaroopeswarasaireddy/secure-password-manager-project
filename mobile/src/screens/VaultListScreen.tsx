import React, { useCallback, useEffect, useState } from 'react';
import { View, Text, FlatList, Button, TextInput, RefreshControl } from 'react-native';
import * as Clipboard from 'expo-clipboard';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';
import { colors } from '../theme/colors';

export default function VaultListScreen({ navigation }: any) {
  const { logout } = useAuth();
  const [data, setData] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setRefreshing(true);
    const res = await api.get('/vault', { params: { search } });
    setData(res.data);
    setRefreshing(false);
  }, [search]);

  useEffect(() => { load(); }, [load]);

  return <View style={{ flex: 1, backgroundColor: colors.bg, padding: 12, gap: 8 }}>
    <TextInput value={search} onChangeText={setSearch} placeholder="Search" placeholderTextColor="#999" style={{ color: colors.text, borderWidth: 1, borderColor: '#3a456a', borderRadius: 8, padding: 8 }} />
    <Button title="Add Password" onPress={() => navigation.navigate('EditPassword')} />
    <Button title="Settings" onPress={() => navigation.navigate('Settings')} />
    <FlatList data={data} keyExtractor={(item) => `${item.id}`} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />} renderItem={({ item }) => (
      <View style={{ backgroundColor: colors.card, padding: 12, marginVertical: 6, borderRadius: 10 }}>
        <Text style={{ color: colors.text }}>{item.site} ({item.username})</Text>
        <Button title="Copy" onPress={() => Clipboard.setStringAsync(item.password)} />
        <Button title="Edit" onPress={() => navigation.navigate('EditPassword', { item })} />
      </View>
    )} />
    <Button title="Logout" onPress={logout} color="#cc3d3d" />
  </View>;
}
