import { createContext, useContext, useEffect, useState } from "react";
import { authApi } from "../api/client";

const AuthContext = createContext(null);
const CLAVE = "zipvacunacion_token";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(CLAVE));
  const [usuario, setUsuario] = useState(null); // { id, username, rol, activo }
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [iniciando, setIniciando] = useState(Boolean(localStorage.getItem(CLAVE)));

  // al recargar la página, recupera el usuario con el token guardado
  useEffect(() => {
    if (!token) return;
    let vivo = true;
    authApi
      .me(token)
      .then((u) => vivo && setUsuario(u))
      .catch(() => {
        if (!vivo) return;
        localStorage.removeItem(CLAVE);
        setToken(null);
      })
      .finally(() => vivo && setIniciando(false));
    return () => {
      vivo = false;
    };
  }, [token]);

  async function login(user, pass) {
    setError(null);
    setCargando(true);
    try {
      const data = await authApi.login(user, pass);
      localStorage.setItem(CLAVE, data.access_token);
      setIniciando(true);
      setToken(data.access_token);
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    } finally {
      setCargando(false);
    }
  }

  async function registrar(user, pass) {
    setError(null);
    setCargando(true);
    try {
      await authApi.registrar(user, pass);
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    } finally {
      setCargando(false);
    }
  }

  function logout() {
    localStorage.removeItem(CLAVE);
    setToken(null);
    setUsuario(null);
  }

  const esAdmin = usuario?.rol === "administrador";

  return (
    <AuthContext.Provider
      value={{ token, usuario, esAdmin, error, cargando, iniciando, login, registrar, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext);
}
