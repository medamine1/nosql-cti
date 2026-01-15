import React, { createContext, useContext, useState, useEffect } from "react";
import { logoutApi } from "./api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      setUser({ token });
      localStorage.setItem("token", token);
    } else {
      setUser(null);
      localStorage.removeItem("token");
    }
  }, [token]);

  const login = (newToken) => setToken(newToken);
  const logout = async () => {
    if (token) {
      try {
        await logoutApi(token);
      } catch (e) {
        // Optionally handle error
      }
    }
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
