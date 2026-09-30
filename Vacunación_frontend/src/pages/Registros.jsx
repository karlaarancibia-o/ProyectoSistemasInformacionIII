import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { campanaApi, pacienteApi, vacunaApi, vacunacionApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

export default function Registros() {
  const { token, esAdmin } = useAuth();
  const [d, setD] = useState({ registros: [], pacientes: [], vacunas: [], campanas: [] });
  const [version, setVersion] = useState(0);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [detalle, setDetalle] = useState(null);

  useEffect(() => {
    let vivo = true;
    Promise.all([vacunacionApi.registros(token), pacienteApi.listar(token), vacunaApi.listar(token), campanaApi.listar(token)])
      .then(([registros, pacientes, vacunas, campanas]) => {
        if (!vivo) return;
        setD({ registros: [...registros].sort((a, b) => b.fecha_aplicacion.localeCompare(a.fecha_aplicacion) || b.id - a.id), pacientes, vacunas, campanas });
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  const paciente = (id) => { const p = d.pacientes.find((x) => x.id === id); return p ? `${p.nombres} ${p.apellidos}` : `#${id}`; };
  const vacuna = (id) => d.vacunas.find((x) => x.id === id)?.nombre ?? `#${id}`;
  const campana = (id) => d.campanas.find((x) => x.id === id)?.nombre ?? `#${id}`;

  async function ver(r) {
    setError("");
    try {
      setDetalle(await vacunacionApi.obtenerRegistro(token, r.id));
    } catch (e) {
      setError(e.message);
    }
  }

  async function eliminar(r) {
    if (!window.confirm("¿Eliminar este registro? Se devuelve la dosis al lote.")) return;
    try {
      await vacunacionApi.eliminarRegistro(token, r.id);
      setVersion((v) => v + 1);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Registros de vacunación</h1>
        <p>Dosis aplicadas, de la más reciente a la más antigua.</p>
      </div>
      {error && <p className="msg error">{error}</p>}
      <section className="tarjeta">
        {cargando ? <p>Cargando…</p> : d.registros.length === 0 ? <p className="vacio">Aún no hay dosis registradas.</p> : (
          <div className="scroll-x">
            <table className="tabla">
              <thead><tr><th>Fecha</th><th>Paciente</th><th>Vacuna</th><th>Dosis</th><th>Campaña</th><th /></tr></thead>
              <tbody>
                {d.registros.map((r) => (
                  <tr key={r.id}>
                    <td>{fmt(r.fecha_aplicacion)}</td>
                    <td>{paciente(r.paciente_id)}</td>
                    <td>{vacuna(r.vacuna_id)}</td>
                    <td>{r.es_refuerzo ? <span className="badge pend">Refuerzo</span> : r.numero_dosis}</td>
                    <td>{campana(r.campana_id)}</td>
                    <td className="celda-acc">
                      <button className="btn sec pequeno" onClick={() => ver(r)}>Detalle</button>
                      {esAdmin && <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(r)}><Icon name="trash" size={18} /></button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {detalle && (
        <section className="tarjeta">
          <div className="fila-titulo">
            <h2><Icon name="syringe" /> Registro #{detalle.id}</h2>
            <button className="btn sec pequeno" onClick={() => setDetalle(null)}>Cerrar</button>
          </div>
          <ul className="lista-reg">
            <li><Icon name="user" /><div><strong>{paciente(detalle.paciente_id)}</strong><small>{vacuna(detalle.vacuna_id)} · {detalle.es_refuerzo ? "refuerzo" : `dosis ${detalle.numero_dosis}`} · {fmt(detalle.fecha_aplicacion)}</small></div></li>
            <li><Icon name="megaphone" /><div><strong>{campana(detalle.campana_id)}</strong><small>Punto #{detalle.punto_id} · lote #{detalle.lote_id}</small></div></li>
          </ul>
        </section>
      )}
    </>
  );
}
