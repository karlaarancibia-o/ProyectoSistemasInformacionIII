import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { antecedenteApi, pacienteApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { paciente_id: "", vacuna: "", fecha_aplicacion: "", numero_dosis: 1, observaciones: "" };
const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

export default function Antecedentes() {
  const { token, esAdmin } = useAuth();
  const [lista, setLista] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [vacunas, setVacunas] = useState([]);
  const [filtro, setFiltro] = useState("");
  const [form, setForm] = useState(VACIO);
  const [detalle, setDetalle] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([antecedenteApi.listar(token, filtro), pacienteApi.listar(token), vacunaApi.listar(token)])
      .then(([a, p, v]) => {
        if (!vivo) return;
        setLista(a);
        setPacientes(p);
        setVacunas(v);
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, filtro, version]);

  const paciente = (id) => {
    const p = pacientes.find((x) => x.id === id);
    return p ? `${p.nombres} ${p.apellidos}` : `#${id}`;
  };
  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));

  async function crear(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    try {
      await antecedenteApi.crear(token, {
        ...form,
        paciente_id: Number(form.paciente_id),
        numero_dosis: Number(form.numero_dosis),
        observaciones: form.observaciones || null,
      });
      setForm(VACIO);
      setMensaje("Antecedente registrado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function ver(a) {
    setError("");
    try {
      setDetalle(await antecedenteApi.obtener(token, a.id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function eliminar(a) {
    if (!window.confirm("¿Eliminar este antecedente?")) return;
    setError("");
    setMensaje("");
    try {
      await antecedenteApi.eliminar(token, a.id);
      if (detalle?.id === a.id) setDetalle(null);
      setMensaje("Antecedente eliminado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Antecedentes de vacunación</h1>
        <p>Dosis recibidas por los pacientes antes de entrar al sistema.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      <form className="tarjeta form-grid" onSubmit={crear}>
        <h2>Nuevo antecedente</h2>
        <label>
          Paciente
          <select value={form.paciente_id} onChange={(e) => set("paciente_id", e.target.value)} required>
            <option value="">Seleccione…</option>
            {pacientes.map((p) => <option key={p.id} value={p.id}>{p.nombres} {p.apellidos}</option>)}
          </select>
        </label>
        <label>
          Vacuna
          <input list="vacunas-ant" value={form.vacuna} onChange={(e) => set("vacuna", e.target.value)} minLength={2} required />
          <datalist id="vacunas-ant">{vacunas.map((v) => <option key={v.id} value={v.nombre} />)}</datalist>
        </label>
        <label>Fecha<input type="date" value={form.fecha_aplicacion} onChange={(e) => set("fecha_aplicacion", e.target.value)} required /></label>
        <label>N.º de dosis<input type="number" min="1" value={form.numero_dosis} onChange={(e) => set("numero_dosis", e.target.value)} required /></label>
        <label className="ancho">Observaciones<input value={form.observaciones} onChange={(e) => set("observaciones", e.target.value)} /></label>
        <div className="acciones ancho"><button className="btn" type="submit">Registrar antecedente</button></div>
      </form>

      <section className="tarjeta">
        <div className="fila-titulo">
          <h2>Antecedentes registrados</h2>
          <select value={filtro} onChange={(e) => setFiltro(e.target.value)}>
            <option value="">Todos los pacientes</option>
            {pacientes.map((p) => <option key={p.id} value={p.id}>{p.nombres} {p.apellidos}</option>)}
          </select>
        </div>
        {cargando ? <p>Cargando…</p> : lista.length === 0 ? <p className="vacio">No hay antecedentes.</p> : (
          <div className="scroll-x">
            <table className="tabla">
              <thead><tr><th>Paciente</th><th>Vacuna</th><th>Fecha</th><th>Dosis</th><th /></tr></thead>
              <tbody>
                {lista.map((a) => (
                  <tr key={a.id} className={detalle?.id === a.id ? "fila-sel" : ""}>
                    <td>{paciente(a.paciente_id)}</td>
                    <td>{a.vacuna}</td>
                    <td>{fmt(a.fecha_aplicacion)}</td>
                    <td>{a.numero_dosis}</td>
                    <td className="celda-acc">
                      <button className="btn sec pequeno" onClick={() => ver(a)}>Detalle</button>
                      {esAdmin && <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(a)}><Icon name="trash" size={18} /></button>}
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
            <h2><Icon name="list" /> Detalle del antecedente</h2>
            <button className="btn sec pequeno" onClick={() => setDetalle(null)}>Cerrar</button>
          </div>
          <ul className="lista-reg">
            <li><Icon name="user" /><div><strong>{paciente(detalle.paciente_id)}</strong><small>Paciente</small></div></li>
            <li><Icon name="syringe" /><div><strong>{detalle.vacuna}</strong><small>Dosis {detalle.numero_dosis} · {fmt(detalle.fecha_aplicacion)}</small></div></li>
            <li><Icon name="list" /><div><strong>Observaciones</strong><small>{detalle.observaciones || "Sin observaciones"}</small></div></li>
          </ul>
        </section>
      )}
    </>
  );
}
