import { createContext, useContext, useEffect, useState } from "react";
import { getCurrentUser, getToken, logout as logoutApi } from "../services/api";
import type { User } from "../types/user";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: () => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    const token = getToken();
    if (token) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error("Failed to get user:", error);
        // 토큰이 유효하지 않은 경우 로그아웃
        await logoutApi();
        setUser(null);
      }
    }
    setLoading(false);
  };

  const login = async () => {
    await checkAuth();
  };

  const logout = () => {
    logoutApi();
    setUser(null);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}