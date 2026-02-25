import React from 'react';
import { View } from 'react-native';
import { colors } from '../theme/colors';

export default function PasswordStrengthMeter({ password }: { password: string }) {
  const score = [/[A-Z]/, /[a-z]/, /\d/, /[^A-Za-z0-9]/].reduce((acc, rule) => acc + (rule.test(password) ? 1 : 0), password.length >= 12 ? 1 : 0);
  const width = `${Math.min((score / 5) * 100, 100)}%` as const;
  return <View style={{ height: 8, backgroundColor: '#2A355C', borderRadius: 8 }}><View style={{ height: 8, width, backgroundColor: score >= 4 ? colors.success : colors.danger, borderRadius: 8 }} /></View>;
}
