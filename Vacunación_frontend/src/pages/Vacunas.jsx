import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { grupoEdadApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = {
  nombre: "",
  fabricante: "",
  tipo: "",
  temperatura_minima: 2,
  temperatura_maxima: 8,
  descripcion: "",
  estado: "activa",
  grupo_edad_ids: [],
};

export default function Vacunas() {
  const { token, esAdmin } = useAuth();
  const [vacunas, setVacunas] = useState([]);
  const [grupos, setGrupos] = useState([]);
  const [form, setForm] = useState(VACIO);
  const [editandoId, setEditandoId] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");

  const [version, setVersion] = useState(0);
  const cargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([vacunaApi.listar(token), grupoEdadApi.listar(token)])
      .then(([v, g]) => {
        if (!vivo) return;
        setVacunas(v);
        setGrupos([...g].sort((a, b) => a.prioridad - b.prioridad));
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  const nombreGrupo = (id) => grupos.find((g) => g.id === id)?.nombre ?? `#${id}`;

  function set(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }));
  }

  function alternarGrupo(id) {
    setForm((f) => ({
      ...f,
      grupo_edad_ids: f.grupo_edad_ids.includes(id)
        ? f.grupo_edad_ids.filter((x) => x !== id)
        : [...f.grupo_edad_ids, id],
    }));
  }

  async function guardar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    if (form.grupo_edad_ids.length === 0) {
      setError("Seleccione al menos un grupo de edad para la vacuna.");
      return;
    }
    const datos = {
      nombre: form.nombre,
      fabricante: form.fabricante,
      tipo: form.tipo,
      temperatura_minima: Number(form.temperatura_minima),
      temperatura_maxima: Number(form.temperatura_maxima),
      descripcion: form.descripcion || null,
      grupo_edad_ids: form.grupo_edad_ids,
    };
    try {
      if (editandoId) await vacunaApi.actualizar(token, editandoId, { ...datos, estado: form.estado });
      else await vacunaApi.crear(token, datos);
      setMensaje(editandoId ? "Vacuna actualizada." : "Vacuna registrada.");
      cancelar();
      cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function editar(vacuna) {
    setError("");
    try {
      const v = await vacunaApi.obtener(token, vacuna.id); // datos frescos del servidor
      setEditandoId(v.id);
      setForm({ ...v, descripcion: v.descripcion || "", grupo_edad_ids: v.grupo_edad_ids || [] });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelar() {
    setEditandoId(null);
    setForm(VACIO);
  }

  async function eliminar(v) {
    if (!window.confirm(`¿Eliminar la vacuna "${v.nombre}"?`)) return;
    setError("");
    setMensaje("");
    try {
      await vacunaApi.eliminar(token, v.id);
      setMensaje("Vacuna eliminada.");
      cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Vacunas</h1>
        <p>Catálogo de vacunas y los grupos de edad a los que está indicada cada una.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {esAdmin && (
        <form className="tarjeta form-grid" onSubmit={guardar}>
          <h2>{editandoId ? "Editar vacuna" : "Nueva vacuna"}</h2>
          <label>
            Nombre
            <input value={form.nombre} onChange={(e) => set("nombre", e.target.value)} placeholder="Ej. Sarampión" minLength={2} required />
          </label>
          <label>
            Fabricante
            <input value={form.fabricante} onChange={(e) => set("fabricante", e.target.value)} minLength={2} required />
          </label>
          <label>
            Tipo
            <input value={form.tipo} onChange={(e) => set("tipo", e.target.value)} placeholder="Ej. Viral" minLength={2} required />
          </label>
          <label>
            Temp. mínima (°C)
            <input type="number" step="0.1" value={form.temperatura_minima} onChange={(e) => set("temperatura_minima", e.target.value)} required />
          </label>
          <label>
            Temp. máxima (°C)
            <input type="number" step="0.1" value={form.temperatura_maxima} onChange={(e) => set("temperatura_maxima", e.target.value)} required />
          </label>
          {editandoId && (
            <label>
              Estado
              <select value={form.estado} onChange={(e) => set("estado", e.target.value)}>
                <option value="activa">Activa</option>
                <option value="inactiva">Inactiva</option>
              </select>
            </label>
          )}
          <label className="ancho">
            Descripción
            <input value={form.descripcion} onChange={(e) => set("descripcion", e.target.value)} />
          </label>

          <fieldset className="ancho grupos-sel">
            <legend>Grupos de edad indicados *</legend>
            {grupos.length === 0 ? (
              <p className="msg error">Primero cree grupos de edad en la sección «Grupos de edad».</p>
            ) : (
              <div className="chips">
                {grupos.map((g) => {
                  const activo = form.grupo_edad_ids.includes(g.id);
                  return (
                    <label key={g.id} className={`chip ${activo ? "on" : ""}`}>
                      <input type="checkbox" checked={activo} onChange={() => alternarGrupo(g.id)} />
                      {activo && <Icon name="check" size={14} />}
                      {g.nombre} <small>({g.edad_min}–{g.edad_max} años)</small>
                    </label>
                  );
                })}
              </div>
            )}
          </fieldset>

          <div className="acciones ancho">
            <button className="btn" type="submit" disabled={grupos.length === 0}>
              {editandoId ? "Guardar cambios" : "Registrar vacuna"}
            </button>
            {editandoId && (
              <button className="btn sec" type="button" onClick={cancelar}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      )}

      <section className="tarjeta">
        <h2>Catálogo</h2>
        {cargando ? (
          <p>Cargando…</p>
        ) : vacunas.length === 0 ? (
          <p className="vacio">Aún no hay vacunas registradas.</p>
        ) : (
          <div className="scroll-x">
            <table className="tabla">
              <thead>
                <tr>
                  <th>Vacuna</th>
                  <th>Fabricante</th>
                  <th>Tipo</th>
                  <th>Temperatura</th>
                  <th>Grupos de edad</th>
                  <th>Estado</th>
                  {esAdmin && <th />}
                </tr>
              </thead>
              <tbody>
                {vacunas.map((v) => (
                  <tr key={v.id}>
                    <td>{v.nombre}</td>
                    <td>{v.fabricante}</td>
                    <td>{v.tipo}</td>
                    <td>
                      {v.temperatura_minima} a {v.temperatura_maxima} °C
                    </td>
                    <td>
                      {(v.grupo_edad_ids || []).length === 0
                        ? "—"
                        : v.grupo_edad_ids.map((id) => (
                            <span key={id} className="badge suave">
                              {nombreGrupo(id)}
                            </span>
                          ))}
                    </td>
                    <td>
                      <span className={`badge ${v.estado === "activa" ? "ok" : "off"}`}>{v.estado}</span>
                    </td>
                    {esAdmin && (
                      <td className="celda-acc">
                        <button className="icon-btn" title="Editar" onClick={() => editar(v)}>
                          <Icon name="edit" size={18} />
                        </button>
                        <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(v)}>
                          <Icon name="trash" size={18} />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  );
}
