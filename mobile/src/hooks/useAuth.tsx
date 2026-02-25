import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import * as SecureStore from 'expo-secure-store';
import api from '../services/api';

type AuthContextType = {
  token: string | null;
  login: (email: string, password: string, totpCode?: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  lock: boolean;
  unlock: () => void;
};

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [lock, setLock] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    SecureStore.getItemAsync('access_token').then(setToken);
  }, []);

  const resetInactivityTimer = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => setLock(true), 5 * 60 * 1000);
  };

  const login = async (email: string, password: string, totpCode?: string) => {
    const { data } = await api.post('/auth/login', { email, password, totp_code: totpCode });
    await SecureStore.setItemAsync('access_token', data.access_token);
    await SecureStore.setItemAsync('refresh_token', data.refresh_token);
    setToken(data.access_token);
    setLock(false);
    resetInactivityTimer();
  };

  const register = async (email: string, password: string) => {
    await api.post('/auth/register', { email, password });
  };

  const logout = async () => {
    const refresh_token = await SecureStore.getItemAsync('refresh_token');
    if (refresh_token) await api.post('/auth/logout', { refresh_token });
    await SecureStore.deleteItemAsync('access_token');
    await SecureStore.deleteItemAsync('refresh_token');
    setToken(null);
  };

  return <AuthContext.Provider value={{ token, login, register, logout, lock, unlock: () => setLock(false) }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
