import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { pacienteApi, vacunaApi, vacunacionApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

export default function Seguimiento() {
  const { token } = useAuth();
  const [vacunas, setVacunas] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [vacunaId, setVacunaId] = useState("");
  const [pendientes, setPendientes] = useState([]);
  const [refuerzos, setRefuerzos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  // consulta individual
  const [pacienteId, setPacienteId] = useState("");
  const [vacunaInd, setVacunaInd] = useState("");
  const [individual, setIndividual] = useState(null);

  useEffect(() => {
    let vivo = true;
    Promise.all([vacunaApi.listar(token), pacienteApi.listar(token)])
      .then(([v, p]) => {
        if (!vivo) return;
        setVacunas(v);
        setPacientes(p);
      })
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token]);

  useEffect(() => {
    if (!vacunaId) return;
    let vivo = true;
    Promise.all([vacunacionApi.dosisPendientes(token, vacunaId), vacunacionApi.refuerzosPendientes(token, vacunaId)])
      .then(([p, r]) => {
        if (!vivo) return;
        setPendientes(p);
        setRefuerzos(r);
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, vacunaId]);

  const paciente = (id) => {
    const p = pacientes.find((x) => x.id === id);
    return p ? `${p.nombres} ${p.apellidos}` : `#${id}`;
  };

  async function consultar(e) {
    e.preventDefault();
    setError("");
    setIndividual(null);
    try {
      const [esquema, refuerzo] = await Promise.all([
        vacunacionApi.dosisPendientesPaciente(token, pacienteId, vacunaInd),
        vacunacionApi.refuerzoPendientePaciente(token, pacienteId, vacunaInd),
      ]);
      setIndividual({ esquema, refuerzo });
    } catch (err) {
      setError(err.message);
    }
  }

  const filas = (lista) =>
    lista.map((x) => (
      <tr key={x.paciente_id}>
        <td>{paciente(x.paciente_id)}</td>
        <td>{x.esquema.dosis_aplicadas} / {x.esquema.dosis_requeridas}</td>
        <td>{x.esquema.proxima_dosis_numero ? (x.esquema.proxima_dosis_es_refuerzo ? "Refuerzo" : `Dosis ${x.esquema.proxima_dosis_numero}`) : "—"}</td>
        <td>{x.esquema.fecha_minima_proxima_dosis ? fmt(x.esquema.fecha_minima_proxima_dosis) : "—"}</td>
      </tr>
    ));

  const encabezado = <thead><tr><th>Paciente</th><th>Dosis aplicadas</th><th>Próxima</th><th>Desde</th></tr></thead>;

  return (
    <>
      <div className="encabezado">
        <h1>Seguimiento de pacientes</h1>
        <p>Pacientes con dosis o refuerzos pendientes, por vacuna, y consulta individual de esquema.</p>
      </div>

      {error && <p className="msg error">{error}</p>}

      <form className="tarjeta form-grid" onSubmit={consultar}>
        <h2><Icon name="users" /> Consulta individual</h2>
        <label>
          Paciente
          <select value={pacienteId} onChange={(e) => setPacienteId(e.target.value)} required>
            <option value="">Seleccione…</option>
            {pacientes.map((p) => <option key={p.id} value={p.id}>{p.nombres} {p.apellidos} · {p.carnet_identidad}</option>)}
          </select>
        </label>
        <label>
          Vacuna
          <select value={vacunaInd} onChange={(e) => setVacunaInd(e.target.value)} required>
            <option value="">Seleccione…</option>
            {vacunas.map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
          </select>
        </label>
        <div className="acciones ancho"><button className="btn" type="submit">Consultar</button></div>
        {individual && (
          <ul className="lista-reg ancho">
            <li><Icon name="syringe" /><div><strong>Dosis</strong><small>{individual.esquema.dosis_aplicadas} aplicadas de {individual.esquema.dosis_requeridas} · {individual.esquema.dosis_pendientes} pendientes</small></div><span className={`badge ${individual.esquema.esquema_completo ? "ok" : "pend"}`}>{individual.esquema.esquema_completo ? "Esquema completo" : "Incompleto"}</span></li>
            <li><Icon name="calendar" /><div><strong>Próxima dosis</strong><small>{individual.esquema.proxima_dosis_numero ? `${individual.esquema.proxima_dosis_es_refuerzo ? "Refuerzo" : `Dosis ${individual.esquema.proxima_dosis_numero}`}${individual.esquema.fecha_minima_proxima_dosis ? ` · desde ${fmt(individual.esquema.fecha_minima_proxima_dosis)}` : ""}` : "Ninguna"}</small></div></li>
            <li><Icon name="check" /><div><strong>Refuerzo</strong><small>{individual.esquema.refuerzos_aplicados} aplicados</small></div><span className={`badge ${individual.refuerzo ? "pend" : "ok"}`}>{individual.refuerzo ? "Refuerzo pendiente" : "Sin refuerzo pendiente"}</span></li>
          </ul>
        )}
      </form>

      <section className="tarjeta form-grid">
        <h2><Icon name="list" /> Pendientes por vacuna</h2>
        <label className="ancho">
          Vacuna
          <select value={vacunaId} onChange={(e) => { setCargando(true); setVacunaId(e.target.value); }}>
            <option value="">Seleccione una vacuna…</option>
            {vacunas.map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
          </select>
        </label>
      </section>

      {vacunaId && (
        <>
          <section className="tarjeta">
            <h2>Pacientes con dosis pendientes ({pendientes.length})</h2>
            {cargando ? <p>Cargando…</p> : pendientes.length === 0 ? <p className="vacio">Nadie tiene dosis pendientes.</p> : (
              <div className="scroll-x"><table className="tabla compacta">{encabezado}<tbody>{filas(pendientes)}</tbody></table></div>
            )}
          </section>
          <section className="tarjeta">
            <h2>Pacientes con refuerzo pendiente ({refuerzos.length})</h2>
            {cargando ? <p>Cargando…</p> : refuerzos.length === 0 ? <p className="vacio">Nadie tiene refuerzos pendientes.</p> : (
              <div className="scroll-x"><table className="tabla compacta">{encabezado}<tbody>{filas(refuerzos)}</tbody></table></div>
            )}
          </section>
        </>
      )}
    </>
  );
}
