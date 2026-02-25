import React from 'react';
import { View, Button } from 'react-native';
import { useAuth } from '../hooks/useAuth';
import { colors } from '../theme/colors';

export default function SettingsScreen() {
  const { logout } = useAuth();
  return <View style={{ flex: 1, backgroundColor: colors.bg, padding: 16, gap: 12 }}>
    <Button title="Logout" onPress={logout} />
  </View>;
}
