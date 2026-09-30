import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { grupoEdadApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { nombre: "", edad_min: 0, edad_max: 11, prioridad: 1, descripcion: "" };

export default function GruposEdad() {
  const { token, esAdmin } = useAuth();
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
    grupoEdadApi
      .listar(token)
      .then((data) => {
        if (!vivo) return;
        setGrupos([...data].sort((a, b) => a.prioridad - b.prioridad));
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  function set(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }));
  }

  async function guardar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    const datos = {
      ...form,
      edad_min: Number(form.edad_min),
      edad_max: Number(form.edad_max),
      prioridad: Number(form.prioridad),
      descripcion: form.descripcion || null,
    };
    try {
      if (editandoId) await grupoEdadApi.actualizar(token, editandoId, datos);
      else await grupoEdadApi.crear(token, datos);
      setMensaje(editandoId ? "Grupo actualizado." : "Grupo creado.");
      cancelar();
      cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function editar(grupo) {
    setError("");
    try {
      const g = await grupoEdadApi.obtener(token, grupo.id); // datos frescos del servidor
      setEditandoId(g.id);
      setForm({ ...g, descripcion: g.descripcion || "" });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err.message);
    }
  }

  async function cambiarPrioridad(g, nueva) {
    if (nueva < 1) return;
    setError("");
    setMensaje("");
    try {
      await grupoEdadApi.editarPrioridad(token, g.id, nueva);
      setMensaje(`Prioridad de "${g.nombre}" actualizada.`);
      cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelar() {
    setEditandoId(null);
    setForm(VACIO);
  }

  async function eliminar(g) {
    if (!window.confirm(`¿Eliminar el grupo "${g.nombre}"?`)) return;
    setError("");
    setMensaje("");
    try {
      await grupoEdadApi.eliminar(token, g.id);
      setMensaje("Grupo eliminado.");
      cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Grupos de edad</h1>
        <p>Rangos de edad que luego se seleccionan al registrar vacunas y campañas.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {esAdmin && (
        <form className="tarjeta form-grid" onSubmit={guardar}>
          <h2>{editandoId ? "Editar grupo" : "Nuevo grupo"}</h2>
          <label>
            Nombre
            <input value={form.nombre} onChange={(e) => set("nombre", e.target.value)} placeholder="Ej. Niños" minLength={2} required />
          </label>
          <label>
            Edad mínima (años)
            <input type="number" min="0" value={form.edad_min} onChange={(e) => set("edad_min", e.target.value)} required />
          </label>
          <label>
            Edad máxima (años)
            <input type="number" min="0" value={form.edad_max} onChange={(e) => set("edad_max", e.target.value)} required />
          </label>
          <label>
            Prioridad (1 = máxima)
            <input type="number" min="1" value={form.prioridad} onChange={(e) => set("prioridad", e.target.value)} required />
          </label>
          <label className="ancho">
            Descripción
            <input value={form.descripcion} onChange={(e) => set("descripcion", e.target.value)} />
          </label>
          <div className="acciones ancho">
            <button className="btn" type="submit">
              {editandoId ? "Guardar cambios" : "Crear grupo"}
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
        <h2>Grupos registrados</h2>
        {cargando ? (
          <p>Cargando…</p>
        ) : grupos.length === 0 ? (
          <p className="vacio">Aún no hay grupos de edad.</p>
        ) : (
          <table className="tabla">
            <thead>
              <tr>
                <th>Prioridad</th>
                <th>Nombre</th>
                <th>Rango</th>
                <th>Descripción</th>
                {esAdmin && <th />}
              </tr>
            </thead>
            <tbody>
              {grupos.map((g) => (
                <tr key={g.id}>
                  <td>
                    {g.prioridad}
                    {esAdmin && (
                      <>
                        {" "}
                        <button className="icon-btn" title="Subir prioridad" onClick={() => cambiarPrioridad(g, g.prioridad - 1)}>▲</button>
                        <button className="icon-btn" title="Bajar prioridad" onClick={() => cambiarPrioridad(g, g.prioridad + 1)}>▼</button>
                      </>
                    )}
                  </td>
                  <td>{g.nombre}</td>
                  <td>
                    {g.edad_min} – {g.edad_max} años
                  </td>
                  <td>{g.descripcion || "—"}</td>
                  {esAdmin && (
                    <td className="celda-acc">
                      <button className="icon-btn" title="Editar" onClick={() => editar(g)}>
                        <Icon name="edit" size={18} />
                      </button>
                      <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(g)}>
                        <Icon name="trash" size={18} />
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  );
}
