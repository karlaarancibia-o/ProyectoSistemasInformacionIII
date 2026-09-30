import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { Icon, Logo } from "./Icons.jsx";

// `roles`: quién ve la opción (el administrador ve todo). Sin `roles`, la ven todos.
const MENU = [
  { to: "/", icon: "home", texto: "Inicio", fin: true },
  { to: "/campanas", icon: "megaphone", texto: "Campañas" },
  { to: "/pacientes", icon: "users", texto: "Pacientes", roles: ["personal_salud"] },
  { to: "/registrar-dosis", icon: "syringe", texto: "Registrar dosis", roles: ["personal_salud"] },
  { to: "/registros", icon: "list", texto: "Registros", roles: ["personal_salud"] },
  { to: "/antecedentes", icon: "list", texto: "Antecedentes", roles: ["personal_salud"] },
  { to: "/seguimiento", icon: "bell", texto: "Seguimiento", roles: ["personal_salud"] },
  { to: "/stock", icon: "box", texto: "Stock de dosis", roles: ["logistica"] },
  { to: "/cadena-frio", icon: "snow", texto: "Cadena de frío", roles: ["logistica"] },
  { to: "/puntos", icon: "pin", texto: "Puntos de vacunación" },
  { to: "/vacunas", icon: "syringe", texto: "Vacunas" },
  { to: "/grupos-edad", icon: "layers", texto: "Grupos de edad" },
  { to: "/esquemas", icon: "layers", texto: "Esquemas de vacunación" },
  { to: "/reportes", icon: "check", texto: "Reporte de cobertura", roles: [] },
  { to: "/perfil", icon: "user", texto: "Perfil" },
];

const ROLES = {
  administrador: "Administrador",
  personal_salud: "Personal de salud",
  logistica: "Logística",
};

export default function Layout() {
  const { usuario, esAdmin, logout } = useAuth();
  const menu = MENU.filter((m) => !m.roles || esAdmin || m.roles.includes(usuario?.rol));

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <Logo />
          <span>Inmunia</span>
        </div>
        <div className="topbar-der">
          <button className="icon-btn" aria-label="Notificaciones">
            <Icon name="bell" size={24} />
          </button>
          <div className="usuario">
            <div className="avatar">
              <Icon name="user" size={22} />
            </div>
            <div>
              <strong>{usuario?.username}</strong>
              <small>{ROLES[usuario?.rol] || usuario?.rol}</small>
            </div>
          </div>
        </div>
      </header>

      <aside className="sidebar">
        <nav>
          {menu.map((m) => (
            <NavLink key={m.to} to={m.to} end={m.fin} className="nav-item">
              <Icon name={m.icon} />
              <span>{m.texto}</span>
            </NavLink>
          ))}
          <hr />
          <button className="nav-item salir" onClick={logout}>
            <Icon name="logout" />
            <span>Cerrar sesión</span>
          </button>
        </nav>
        <div className="ola" />
      </aside>

      <main className="contenido">
        <Outlet />
      </main>
    </div>
  );
}
