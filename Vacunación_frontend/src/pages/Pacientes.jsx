import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { grupoEdadApi, pacienteApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { nombres: "", apellidos: "", carnet_identidad: "", fecha_nacimiento: "", sexo: "M", telefono: "", direccion: "" };
const ANT_VACIO = { vacuna: "", fecha_aplicacion: "", numero_dosis: 1, observaciones: "" };
const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

export default function Pacientes() {
  const { token, esAdmin } = useAuth();
  const [pacientes, setPacientes] = useState([]);
  const [grupos, setGrupos] = useState([]);
  const [vacunas, setVacunas] = useState([]);
  const [form, setForm] = useState(VACIO);
  const [busqueda, setBusqueda] = useState("");
  const [version, setVersion] = useState(0);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [sel, setSel] = useState(null); // paciente con historial abierto
  const [historial, setHistorial] = useState(null);
  const [ant, setAnt] = useState(ANT_VACIO);
  const [ficha, setFicha] = useState(null); // datos actualizados del paciente abierto

  useEffect(() => {
    let vivo = true;
    Promise.all([pacienteApi.listar(token), grupoEdadApi.listar(token), vacunaApi.listar(token)])
      .then(([p, g, v]) => {
        if (!vivo) return;
        setPacientes(p);
        setGrupos(g);
        setVacunas(v);
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  useEffect(() => {
    if (!sel) return;
    let vivo = true;
    pacienteApi.historial(token, sel.id).then((h) => vivo && setHistorial(h)).catch((e) => vivo && setError(e.message));
    pacienteApi.obtener(token, sel.id).then((p) => vivo && setFicha(p)).catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token, sel, version]);

  const recargar = () => setVersion((v) => v + 1);
  const nombreGrupo = (id) => grupos.find((g) => g.id === id)?.nombre ?? "—";
  const nombreVacuna = (id) => vacunas.find((v) => v.id === id)?.nombre ?? `#${id}`;
  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));

  const visibles = pacientes.filter((p) => {
    const q = busqueda.trim().toLowerCase();
    return !q || `${p.nombres} ${p.apellidos} ${p.carnet_identidad}`.toLowerCase().includes(q);
  });

  async function crear(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    try {
      await pacienteApi.crear(token, { ...form, telefono: form.telefono || null, direccion: form.direccion || null });
      setForm(VACIO);
      setMensaje("Paciente registrado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function eliminar(p) {
    if (!window.confirm(`¿Eliminar a ${p.nombres} ${p.apellidos}?`)) return;
    setError("");
    try {
      await pacienteApi.eliminar(token, p.id);
      if (sel?.id === p.id) abrir(null);
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  function abrir(p) {
    setSel(p);
    setFicha(null);
    setHistorial(null);
    setAnt(ANT_VACIO);
  }

  async function agregarAntecedente(e) {
    e.preventDefault();
    setError("");
    try {
      await pacienteApi.agregarAntecedente(token, sel.id, { ...ant, numero_dosis: Number(ant.numero_dosis), observaciones: ant.observaciones || null });
      setAnt(ANT_VACIO);
      setMensaje("Antecedente registrado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Pacientes</h1>
        <p>Registro de pacientes, su grupo de edad y su historial de vacunación.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      <form className="tarjeta form-grid" onSubmit={crear}>
        <h2>Nuevo paciente</h2>
        <label>Nombres<input value={form.nombres} onChange={(e) => set("nombres", e.target.value)} minLength={2} required /></label>
        <label>Apellidos<input value={form.apellidos} onChange={(e) => set("apellidos", e.target.value)} minLength={2} required /></label>
        <label>Carnet de identidad<input value={form.carnet_identidad} onChange={(e) => set("carnet_identidad", e.target.value)} minLength={2} required /></label>
        <label>Fecha de nacimiento<input type="date" value={form.fecha_nacimiento} onChange={(e) => set("fecha_nacimiento", e.target.value)} required /></label>
        <label>Sexo<select value={form.sexo} onChange={(e) => set("sexo", e.target.value)}><option value="M">Masculino</option><option value="F">Femenino</option></select></label>
        <label>Teléfono<input value={form.telefono} onChange={(e) => set("telefono", e.target.value)} /></label>
        <label className="ancho">Dirección<input value={form.direccion} onChange={(e) => set("direccion", e.target.value)} /></label>
        <div className="acciones ancho"><button className="btn" type="submit">Registrar paciente</button></div>
      </form>

      <section className="tarjeta">
        <div className="fila-titulo">
          <h2>Pacientes registrados</h2>
          <input className="filtro" placeholder="Filtrar por nombre o CI…" value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />
        </div>
        {cargando ? <p>Cargando…</p> : visibles.length === 0 ? <p className="vacio">No hay pacientes.</p> : (
          <div className="scroll-x">
            <table className="tabla">
              <thead><tr><th>Paciente</th><th>CI</th><th>Nacimiento</th><th>Sexo</th><th>Grupo de edad</th><th /></tr></thead>
              <tbody>
                {visibles.map((p) => (
                  <tr key={p.id} className={sel?.id === p.id ? "fila-sel" : ""}>
                    <td>{p.nombres} {p.apellidos}</td>
                    <td>{p.carnet_identidad}</td>
                    <td>{fmt(p.fecha_nacimiento)}</td>
                    <td>{p.sexo}</td>
                    <td>{p.grupo_edad_id ? <span className="badge suave">{nombreGrupo(p.grupo_edad_id)}</span> : "—"}</td>
                    <td className="celda-acc">
                      <button className="btn sec pequeno" onClick={() => abrir(p)}>Historial</button>
                      {esAdmin && <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(p)}><Icon name="trash" size={18} /></button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {sel && (
        <section className="tarjeta">
          <div className="fila-titulo">
            <h2><Icon name="list" /> Historial de {sel.nombres} {sel.apellidos}</h2>
            <button className="btn sec pequeno" onClick={() => abrir(null)}>Cerrar</button>
          </div>
          {!historial ? <p>Cargando…</p> : (
            <>
              {ficha && (
                <p className="vacio">
                  CI {ficha.carnet_identidad} · nació el {fmt(ficha.fecha_nacimiento)} · {ficha.sexo === "M" ? "Masculino" : "Femenino"} · {nombreGrupo(ficha.grupo_edad_id)}
                  {ficha.telefono ? ` · Tel. ${ficha.telefono}` : ""}{ficha.direccion ? ` · ${ficha.direccion}` : ""}
                </p>
              )}
              <h3>Dosis aplicadas en el sistema</h3>
              {historial.dosis_aplicadas_en_el_sistema.length === 0 ? <p className="vacio">Ninguna todavía.</p> : (
                <ul className="lista-reg">
                  {historial.dosis_aplicadas_en_el_sistema.map((r) => (
                    <li key={r.id}><Icon name="syringe" /><div><strong>{nombreVacuna(r.vacuna_id)}</strong><small>{fmt(r.fecha_aplicacion)} · dosis {r.numero_dosis}{r.es_refuerzo ? " (refuerzo)" : ""}</small></div><span className="badge ok">Aplicada</span></li>
                  ))}
                </ul>
              )}
              <h3>Antecedentes (dosis previas fuera del sistema)</h3>
              {historial.antecedentes.length === 0 ? <p className="vacio">Sin antecedentes.</p> : (
                <ul className="lista-reg">
                  {historial.antecedentes.map((a) => (
                    <li key={a.id}><Icon name="syringe" /><div><strong>{a.vacuna}</strong><small>{fmt(a.fecha_aplicacion)} · dosis {a.numero_dosis}{a.observaciones ? ` · ${a.observaciones}` : ""}</small></div></li>
                  ))}
                </ul>
              )}
              <form className="form-grid sub" onSubmit={agregarAntecedente}>
                <h3>Agregar antecedente</h3>
                <label>Vacuna<input list="vacunas-lista" value={ant.vacuna} onChange={(e) => setAnt({ ...ant, vacuna: e.target.value })} minLength={2} required /></label>
                <datalist id="vacunas-lista">{vacunas.map((v) => <option key={v.id} value={v.nombre} />)}</datalist>
                <label>Fecha<input type="date" value={ant.fecha_aplicacion} onChange={(e) => setAnt({ ...ant, fecha_aplicacion: e.target.value })} required /></label>
                <label>N.º de dosis<input type="number" min="1" value={ant.numero_dosis} onChange={(e) => setAnt({ ...ant, numero_dosis: e.target.value })} required /></label>
                <label>Observaciones<input value={ant.observaciones} onChange={(e) => setAnt({ ...ant, observaciones: e.target.value })} /></label>
                <div className="acciones ancho"><button className="btn" type="submit">Agregar</button></div>
              </form>
            </>
          )}
        </section>
      )}
    </>
  );
}
