import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { puntoApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { nombre: "", direccion: "", telefono: "", capacidad: 50, estado: "activo" };
const DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
const HORARIO_VACIO = { dia_semana: 0, hora_apertura: "08:00", hora_cierre: "16:00" };
const hhmm = (t) => (t ? t.slice(0, 5) : "");

export default function Puntos() {
  const { token, esAdmin } = useAuth();
  const [puntos, setPuntos] = useState([]);
  const [form, setForm] = useState(VACIO);
  const [editandoId, setEditandoId] = useState(null);
  const [abierto, setAbierto] = useState(null); // punto cuyos horarios se muestran
  const [horarios, setHorarios] = useState([]);
  const [horarioForm, setHorarioForm] = useState(HORARIO_VACIO);
  const [horarioEditId, setHorarioEditId] = useState(null);
  const [alertas, setAlertas] = useState({ sinStock: [], pendientes: [] });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    puntoApi
      .listar(token)
      .then((data) => {
        if (!vivo) return;
        setPuntos([...data].sort((a, b) => a.nombre.localeCompare(b.nombre)));
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  useEffect(() => {
    if (!abierto) return;
    let vivo = true;
    puntoApi
      .horarios(token, abierto)
      .then((h) => vivo && setHorarios([...h].sort((a, b) => a.dia_semana - b.dia_semana)))
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token, abierto, version]);

  useEffect(() => {
    // Alertas solo para roles con acceso (administrador / logística); el resto las ignora.
    let vivo = true;
    Promise.all([puntoApi.sinStock(token), puntoApi.temperaturasPendientes(token)])
      .then(([sinStock, pendientes]) => vivo && setAlertas({ sinStock, pendientes }))
      .catch(() => vivo && setAlertas({ sinStock: [], pendientes: [] }));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));

  async function guardar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    const datos = { ...form, capacidad: Number(form.capacidad), telefono: form.telefono || null };
    try {
      if (editandoId) await puntoApi.actualizar(token, editandoId, datos);
      else await puntoApi.crear(token, datos);
      setMensaje(editandoId ? "Punto actualizado." : "Punto creado.");
      cancelar();
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function editar(punto) {
    setError("");
    try {
      const p = await puntoApi.obtener(token, punto.id); // datos frescos del servidor
      setEditandoId(p.id);
      setForm({ nombre: p.nombre, direccion: p.direccion, telefono: p.telefono || "", capacidad: p.capacidad, estado: p.estado });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelar() {
    setEditandoId(null);
    setForm(VACIO);
  }

  async function eliminar(p) {
    if (!window.confirm(`¿Eliminar el punto "${p.nombre}"?`)) return;
    setError("");
    setMensaje("");
    try {
      await puntoApi.eliminar(token, p.id);
      if (abierto === p.id) setAbierto(null);
      setMensaje("Punto eliminado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function editarHorario(h) {
    setError("");
    try {
      const x = await puntoApi.obtenerHorario(token, abierto, h.id);
      setHorarioEditId(x.id);
      setHorarioForm({ dia_semana: x.dia_semana, hora_apertura: hhmm(x.hora_apertura), hora_cierre: hhmm(x.hora_cierre) });
    } catch (err) {
      setError(err.message);
    }
  }

  async function agregarHorario(e) {
    e.preventDefault();
    setError("");
    try {
      const datos = {
        dia_semana: Number(horarioForm.dia_semana),
        hora_apertura: horarioForm.hora_apertura,
        hora_cierre: horarioForm.hora_cierre,
      };
      if (horarioEditId) await puntoApi.actualizarHorario(token, abierto, horarioEditId, datos);
      else await puntoApi.definirHorario(token, abierto, datos);
      setHorarioEditId(null);
      setHorarioForm(HORARIO_VACIO);
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function quitarHorario(h) {
    setError("");
    try {
      await puntoApi.eliminarHorario(token, abierto, h.id);
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  const puntoAbierto = puntos.find((p) => p.id === abierto);

  return (
    <>
      <div className="encabezado">
        <h1>Puntos de vacunación</h1>
        <p>Centros donde se aplican las dosis, con su capacidad y horarios de atención.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {(alertas.sinStock.length > 0 || alertas.pendientes.length > 0) && (
        <section className="tarjeta">
          <h2><Icon name="bell" /> Alertas de puntos</h2>
          {alertas.sinStock.map((p) => <p key={`s${p.id}`} className="aviso">Sin stock: {p.nombre} no tiene dosis disponibles.</p>)}
          {alertas.pendientes.map((p) => <p key={`t${p.id}`} className="aviso">Temperatura pendiente: {p.nombre} aún no registra la temperatura de hoy.</p>)}
        </section>
      )}

      {esAdmin && (
        <form className="tarjeta form-grid" onSubmit={guardar}>
          <h2>{editandoId ? "Editar punto" : "Nuevo punto"}</h2>
          <label>
            Nombre
            <input value={form.nombre} onChange={(e) => set("nombre", e.target.value)} minLength={2} required />
          </label>
          <label>
            Dirección
            <input value={form.direccion} onChange={(e) => set("direccion", e.target.value)} minLength={2} required />
          </label>
          <label>
            Teléfono
            <input value={form.telefono} onChange={(e) => set("telefono", e.target.value)} />
          </label>
          <label>
            Capacidad (personas/día)
            <input type="number" min="1" value={form.capacidad} onChange={(e) => set("capacidad", e.target.value)} required />
          </label>
          <label>
            Estado
            <select value={form.estado} onChange={(e) => set("estado", e.target.value)}>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
            </select>
          </label>
          <div className="acciones ancho">
            <button className="btn" type="submit">{editandoId ? "Guardar cambios" : "Crear punto"}</button>
            {editandoId && <button className="btn sec" type="button" onClick={cancelar}>Cancelar</button>}
          </div>
        </form>
      )}

      <section className="tarjeta">
        <h2>Puntos registrados</h2>
        {cargando ? (
          <p>Cargando…</p>
        ) : puntos.length === 0 ? (
          <p className="vacio">Aún no hay puntos de vacunación.</p>
        ) : (
          <div className="scroll-x">
            <table className="tabla">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Dirección</th>
                  <th>Teléfono</th>
                  <th>Capacidad</th>
                  <th>Campañas</th>
                  <th>Estado</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {puntos.map((p) => (
                  <tr key={p.id} className={abierto === p.id ? "fila-sel" : ""}>
                    <td>{p.nombre}</td>
                    <td>{p.direccion}</td>
                    <td>{p.telefono || "—"}</td>
                    <td>{p.capacidad}</td>
                    <td>{p.campana_ids?.length ?? 0}</td>
                    <td><span className={`badge ${p.estado === "activo" ? "ok" : "off"}`}>{p.estado}</span></td>
                    <td className="celda-acc">
                      <button className="btn sec pequeno" onClick={() => setAbierto(abierto === p.id ? null : p.id)}>
                        Horarios
                      </button>
                      {esAdmin && (
                        <>
                          <button className="icon-btn" title="Editar" onClick={() => editar(p)}><Icon name="edit" size={18} /></button>
                          <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(p)}><Icon name="trash" size={18} /></button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {puntoAbierto && (
        <section className="tarjeta">
          <h2><Icon name="calendar" /> Horarios de atención — {puntoAbierto.nombre}</h2>
          {horarios.length === 0 ? (
            <p className="vacio">Este punto todavía no tiene horarios definidos.</p>
          ) : (
            <ul className="lista-reg">
              {horarios.map((h) => (
                <li key={h.id}>
                  <div>
                    <strong>{DIAS[h.dia_semana]}</strong>
                    <small>{hhmm(h.hora_apertura)} – {hhmm(h.hora_cierre)}</small>
                  </div>
                  {esAdmin && (
                    <>
                      <button className="icon-btn" title="Editar" onClick={() => editarHorario(h)}><Icon name="edit" size={18} /></button>
                      <button className="icon-btn peligro" title="Quitar" onClick={() => quitarHorario(h)}><Icon name="trash" size={18} /></button>
                    </>
                  )}
                </li>
              ))}
            </ul>
          )}
          {esAdmin && (
            <form className="form-grid sub" onSubmit={agregarHorario}>
              <h3>{horarioEditId ? "Editar horario" : "Agregar horario"}</h3>
              <label>
                Día
                <select value={horarioForm.dia_semana} onChange={(e) => setHorarioForm((f) => ({ ...f, dia_semana: e.target.value }))}>
                  {DIAS.map((d, i) => <option key={d} value={i}>{d}</option>)}
                </select>
              </label>
              <label>
                Apertura
                <input type="time" value={horarioForm.hora_apertura} onChange={(e) => setHorarioForm((f) => ({ ...f, hora_apertura: e.target.value }))} required />
              </label>
              <label>
                Cierre
                <input type="time" value={horarioForm.hora_cierre} onChange={(e) => setHorarioForm((f) => ({ ...f, hora_cierre: e.target.value }))} required />
              </label>
              <div className="acciones">
                <button className="btn" type="submit">{horarioEditId ? "Guardar horario" : "Agregar"}</button>
                {horarioEditId && <button className="btn sec" type="button" onClick={() => { setHorarioEditId(null); setHorarioForm(HORARIO_VACIO); }}>Cancelar</button>}
              </div>
            </form>
          )}
        </section>
      )}
    </>
  );
}
