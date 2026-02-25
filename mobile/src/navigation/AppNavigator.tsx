import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuth } from '../hooks/useAuth';
import AuthGuard from '../components/AuthGuard';
import SplashScreen from '../screens/SplashScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import VaultListScreen from '../screens/VaultListScreen';
import EditPasswordScreen from '../screens/EditPasswordScreen';
import PasswordGeneratorScreen from '../screens/PasswordGeneratorScreen';
import SettingsScreen from '../screens/SettingsScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const { token, lock } = useAuth();

  if (!token) {
    return (
      <Stack.Navigator>
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
      </Stack.Navigator>
    );
  }

  return (
    <AuthGuard>
      <Stack.Navigator>
        <Stack.Screen name="Vault" component={VaultListScreen} />
        <Stack.Screen name="EditPassword" component={EditPasswordScreen} />
        <Stack.Screen name="Generator" component={PasswordGeneratorScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </AuthGuard>
  );
}
