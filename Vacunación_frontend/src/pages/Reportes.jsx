import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { campanaApi, reporteApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

function Stat({ icon, titulo, valor, pie }) {
  return (
    <div className="tarjeta stat">
      <div className="stat-ico"><Icon name={icon} size={28} /></div>
      <div>
        <small>{titulo}</small>
        <strong>{valor}</strong>
        <small>{pie}</small>
      </div>
    </div>
  );
}

export default function Reportes() {
  const { token } = useAuth();
  const [campanas, setCampanas] = useState([]);
  const [vacunas, setVacunas] = useState([]);
  const [campanaId, setCampanaId] = useState("");
  const [campana, setCampana] = useState(null);
  const [reporte, setReporte] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let vivo = true;
    Promise.all([campanaApi.listar(token), vacunaApi.listar(token)])
      .then(([c, v]) => {
        if (!vivo) return;
        setCampanas(c);
        setVacunas(v);
      })
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token]);

  useEffect(() => {
    if (!campanaId) return;
    let vivo = true;
    Promise.all([campanaApi.obtener(token, campanaId), reporteApi.cobertura(token, campanaId)])
      .then(([c, r]) => {
        if (!vivo) return;
        setCampana(c);
        setReporte(r);
        setError("");
      })
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token, campanaId]);

  const elegir = (id) => {
    setCampanaId(id);
    setCampana(null);
    setReporte(null);
  };
  const nombreVacuna = (id) => vacunas.find((v) => v.id === id)?.nombre ?? `#${id}`;
  const pct = reporte ? Math.min(100, Math.max(0, reporte.porcentaje_cobertura)) : 0;

  return (
    <>
      <div className="encabezado">
        <h1>Reporte de cobertura</h1>
        <p>Avance de vacunación de cada campaña respecto a su población objetivo.</p>
      </div>

      {error && <p className="msg error">{error}</p>}

      <section className="tarjeta form-grid">
        <label className="ancho">
          Campaña
          <select value={campanaId} onChange={(e) => elegir(e.target.value)}>
            <option value="">Seleccione una campaña…</option>
            {campanas.map((c) => <option key={c.id} value={c.id}>{c.nombre} ({c.estado})</option>)}
          </select>
        </label>
      </section>

      {campana && reporte && (
        <>
          <section className="tarjeta">
            <h2><Icon name="megaphone" /> {reporte.nombre_campana}</h2>
            <p className="vacio">
              {campana.tipo_temporada} · {nombreVacuna(campana.vacuna_id)} · {fmt(campana.fecha_inicio)} → {fmt(campana.fecha_fin)} · {campana.punto_ids.length} puntos · {campana.grupo_edad_ids.length || "todos los"} grupos de edad
            </p>
            <span className={`badge ${campana.estado === "activa" ? "ok" : campana.estado === "planificada" ? "pend" : "off"}`}>{campana.estado}</span>
          </section>

          <div className="stats">
            <Stat icon="users" titulo="Población objetivo" valor={reporte.total_pacientes_objetivo} pie="Pacientes en los grupos de la campaña" />
            <Stat icon="users" titulo="Pacientes vacunados" valor={reporte.pacientes_vacunados} pie="Con al menos una dosis" />
            <Stat icon="syringe" titulo="Dosis aplicadas" valor={reporte.total_dosis_aplicadas} pie={`${reporte.total_pacientes_registrados} pacientes registrados`} />
          </div>

        </>
      )}
    </>
  );
}
