import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { Logo } from "../components/Icons.jsx";

export default function Login() {
  const { login, registrar, error, cargando } = useAuth();
  const [modo, setModo] = useState("login"); // login | registro
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const [aviso, setAviso] = useState("");

  async function enviar(e) {
    e.preventDefault();
    setAviso("");
    if (modo === "login") {
      await login(user, password);
    } else if (await registrar(user, password)) {
      setAviso("Cuenta creada. Ahora puedes iniciar sesión.");
      setModo("login");
      setPassword("");
    }
  }

  return (
    <div className="login">
      <form className="login-card" onSubmit={enviar}>
        <div className="login-logo">
          <Logo size={64} color="#c1121f" />
          <h1>Inmunia</h1>
          <p>Las vacunas protegen tu vida</p>
        </div>

        <label>
          Usuario
          <input value={user} onChange={(e) => setUser(e.target.value)} minLength={2} required />
        </label>
        <label>
          Contraseña
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={modo === "registro" ? 6 : undefined}
            required
          />
        </label>

        {error && <p className="msg error">{error}</p>}
        {aviso && <p className="msg ok">{aviso}</p>}

        <button className="btn" type="submit" disabled={cargando}>
          {cargando ? "Procesando…" : modo === "login" ? "Iniciar sesión" : "Crear cuenta"}
        </button>
        <button
          type="button"
          className="link"
          onClick={() => {
            setModo(modo === "login" ? "registro" : "login");
            setAviso("");
          }}
        >
          {modo === "login" ? "¿No tienes cuenta? Regístrate" : "Ya tengo cuenta"}
        </button>
      </form>
    </div>
  );
}
