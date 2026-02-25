import React, { useState } from 'react';
import { View, Text, Button } from 'react-native';
import * as Clipboard from 'expo-clipboard';
import { generatePassword } from '../components/Generator';
import { colors } from '../theme/colors';

export default function PasswordGeneratorScreen() {
  const [pwd, setPwd] = useState(generatePassword());
  return <View style={{ flex: 1, backgroundColor: colors.bg, padding: 16, gap: 12 }}>
    <Text style={{ color: colors.text }}>{pwd}</Text>
    <Button title="Regenerate" onPress={() => setPwd(generatePassword())} />
    <Button title="Copy" onPress={() => Clipboard.setStringAsync(pwd)} />
  </View>;
}
