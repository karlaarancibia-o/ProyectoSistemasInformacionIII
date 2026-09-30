import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./context/AuthContext.jsx";
import Layout from "./components/Layout.jsx";
import Login from "./pages/Login.jsx";
import Inicio from "./pages/Inicio.jsx";
import GruposEdad from "./pages/GruposEdad.jsx";
import Vacunas from "./pages/Vacunas.jsx";
import Campanas from "./pages/Campanas.jsx";
import Pacientes from "./pages/Pacientes.jsx";
import RegistrarDosis from "./pages/RegistrarDosis.jsx";
import Registros from "./pages/Registros.jsx";
import Puntos from "./pages/Puntos.jsx";
import Stock from "./pages/Stock.jsx";
import CadenaFrio from "./pages/CadenaFrio.jsx";
import Perfil from "./pages/Perfil.jsx";
import Esquemas from "./pages/Esquemas.jsx";
import Seguimiento from "./pages/Seguimiento.jsx";
import Reportes from "./pages/Reportes.jsx";
import Antecedentes from "./pages/Antecedentes.jsx";

export default function App() {
  const { token, usuario, iniciando } = useAuth();

  if (iniciando) return <p className="cargando-pantalla">Cargando…</p>;
  if (!token || !usuario) return <Login />;

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Inicio />} />
        <Route path="vacunas" element={<Vacunas />} />
        <Route path="grupos-edad" element={<GruposEdad />} />
        <Route path="campanas" element={<Campanas />} />
        <Route path="pacientes" element={<Pacientes />} />
        <Route path="registrar-dosis" element={<RegistrarDosis />} />
        <Route path="registros" element={<Registros />} />
        <Route path="puntos" element={<Puntos />} />
        <Route path="stock" element={<Stock />} />
        <Route path="cadena-frio" element={<CadenaFrio />} />
        <Route path="esquemas" element={<Esquemas />} />
        <Route path="seguimiento" element={<Seguimiento />} />
        <Route path="antecedentes" element={<Antecedentes />} />
        <Route path="reportes" element={<Reportes />} />
        <Route path="perfil" element={<Perfil />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
