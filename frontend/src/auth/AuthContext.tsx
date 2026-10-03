import { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser, loginUser } from "../services/api";

type User = {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
};

type AuthContextValue = {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  async function login(email: string, password: string) {
    const data = await loginUser({
      email,
      password,
    });

    localStorage.setItem("access_token", data.access_token);

    const currentUser = await getCurrentUser();

    setUser(currentUser);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  useEffect(() => {
    async function loadCurrentUser() {
      try {
        const currentUser = await getCurrentUser();

        setUser(currentUser);
      } catch {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    loadCurrentUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
