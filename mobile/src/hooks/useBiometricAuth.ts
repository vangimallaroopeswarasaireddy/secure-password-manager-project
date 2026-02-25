import * as LocalAuthentication from 'expo-local-authentication';

export async function useBiometricAuth(): Promise<boolean> {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const enrolled = await LocalAuthentication.isEnrolledAsync();
  if (!hasHardware || !enrolled) return false;
  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Unlock Secure Password Manager',
    fallbackLabel: 'Use passcode'
  });
  return result.success;
}
