import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { useBiometricAuth } from '../hooks/useBiometricAuth';
import { colors } from '../theme/colors';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);
  const [allowed, setAllowed] = useState(false);

  useEffect(() => {
    useBiometricAuth().then(ok => {
      setAllowed(ok);
      setReady(true);
    });
  }, []);

  if (!ready) return <ActivityIndicator color={colors.primary} />;
  if (!allowed) return <View><Text style={{ color: colors.text }}>Biometric unlock failed</Text></View>;
  return <>{children}</>;
}
