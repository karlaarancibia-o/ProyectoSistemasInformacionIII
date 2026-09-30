import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { authApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const ROLES = { administrador: "Administrador", personal_salud: "Personal de salud", logistica: "Logística" };
const NUEVO = { username: "", password: "", rol: "personal_salud" };

export default function Perfil() {
  const { token, usuario, esAdmin, logout } = useAuth();
  const [roles, setRoles] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [nuevo, setNuevo] = useState(NUEVO);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    authApi.roles(token).then((r) => vivo && setRoles(r)).catch(() => {});
    return () => {
      vivo = false;
    };
  }, [token]);

  useEffect(() => {
    if (!esAdmin) return;
    let vivo = true;
    authApi
      .usuarios(token)
      .then((u) => vivo && setUsuarios(u))
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token, esAdmin, version]);

  const descripcion = roles.find((r) => r.rol === usuario.rol)?.descripcion;

  async function accion(fn, textoOk) {
    setError("");
    setMensaje("");
    try {
      await fn();
      setMensaje(textoOk);
      recargar();
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    }
  }

  async function crear(e) {
    e.preventDefault();
    const ok = await accion(() => authApi.registrar(nuevo.username, nuevo.password, nuevo.rol, token), "Cuenta creada.");
    if (ok) setNuevo(NUEVO);
  }

  return (
    <>
      <div className="encabezado">
        <h1>Perfil</h1>
        <p>Tu cuenta{esAdmin ? " y la administración de usuarios." : "."}</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      <section className="tarjeta">
        <h2><Icon name="user" /> Mi cuenta</h2>
        <ul className="info">
          <li><div><strong>{usuario.username}</strong><small>Usuario</small></div></li>
          <li>
            <div>
              <strong>{ROLES[usuario.rol] || usuario.rol}</strong>
              <small>{descripcion || "Rol"}</small>
            </div>
          </li>
          <li><div><strong>{usuario.activo ? "Activa" : "Inactiva"}</strong><small>Estado de la cuenta</small></div></li>
        </ul>
        <div className="acciones" style={{ marginTop: 16 }}>
          <button className="btn sec" onClick={logout}>Cerrar sesión</button>
        </div>
      </section>

      {esAdmin && (
        <>
          <form className="tarjeta form-grid" onSubmit={crear}>
            <h2><Icon name="plus" /> Nueva cuenta</h2>
            <label>
              Usuario
              <input value={nuevo.username} onChange={(e) => setNuevo({ ...nuevo, username: e.target.value })} minLength={2} maxLength={50} required />
            </label>
            <label>
              Contraseña (mín. 6)
              <input type="password" value={nuevo.password} onChange={(e) => setNuevo({ ...nuevo, password: e.target.value })} minLength={6} required />
            </label>
            <label>
              Rol
              <select value={nuevo.rol} onChange={(e) => setNuevo({ ...nuevo, rol: e.target.value })}>
                {Object.entries(ROLES).map(([v, t]) => <option key={v} value={v}>{t}</option>)}
              </select>
            </label>
            <div className="acciones"><button className="btn" type="submit">Crear cuenta</button></div>
          </form>

          <section className="tarjeta">
            <h2><Icon name="users" /> Usuarios del sistema</h2>
            <div className="scroll-x">
              <table className="tabla compacta">
                <thead><tr><th>Usuario</th><th>Rol</th><th>Estado</th><th /></tr></thead>
                <tbody>
                  {usuarios.map((u) => {
                    const yo = u.id === usuario.id;
                    return (
                      <tr key={u.id}>
                        <td>{u.username}{yo && <small> (tú)</small>}</td>
                        <td>
                          <select
                            value={u.rol}
                            disabled={yo}
                            onChange={(e) => accion(() => authApi.cambiarRol(token, u.id, e.target.value), "Rol actualizado.")}
                          >
                            {Object.entries(ROLES).map(([v, t]) => <option key={v} value={v}>{t}</option>)}
                          </select>
                        </td>
                        <td><span className={`badge ${u.activo ? "ok" : "off"}`}>{u.activo ? "Activa" : "Inactiva"}</span></td>
                        <td className="celda-acc">
                          {!yo && (
                            <button
                              className="btn sec pequeno"
                              onClick={() => accion(() => authApi.cambiarEstado(token, u.id, !u.activo), u.activo ? "Cuenta desactivada." : "Cuenta activada.")}
                            >
                              {u.activo ? "Desactivar" : "Activar"}
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </>
  );
}
