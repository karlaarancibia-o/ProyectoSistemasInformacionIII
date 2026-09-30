import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { esquemaApi, grupoEdadApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { vacuna_id: "", grupo_edad_id: "", cantidad_dosis: 1, dias_entre_dosis: 0, requiere_refuerzo: false, meses_refuerzo: "" };

export default function Esquemas() {
  const { token, esAdmin } = useAuth();
  const [esquemas, setEsquemas] = useState([]);
  const [vacunas, setVacunas] = useState([]);
  const [grupos, setGrupos] = useState([]);
  const [form, setForm] = useState(VACIO);
  const [editandoId, setEditandoId] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([esquemaApi.listar(token), vacunaApi.listar(token), grupoEdadApi.listar(token)])
      .then(([e, v, g]) => {
        if (!vivo) return;
        setEsquemas(e);
        setVacunas(v);
        setGrupos(g);
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  const nombreVacuna = (id) => vacunas.find((v) => v.id === id)?.nombre ?? `#${id}`;
  const nombreGrupo = (id) => grupos.find((g) => g.id === id)?.nombre ?? `#${id}`;
  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));
  const vacunaSel = vacunas.find((v) => v.id === Number(form.vacuna_id));
  const gruposPosibles = vacunaSel ? grupos.filter((g) => vacunaSel.grupo_edad_ids?.includes(g.id)) : grupos;

  async function guardar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    const datos = {
      vacuna_id: Number(form.vacuna_id),
      grupo_edad_id: Number(form.grupo_edad_id),
      cantidad_dosis: Number(form.cantidad_dosis),
      dias_entre_dosis: Number(form.dias_entre_dosis),
      requiere_refuerzo: form.requiere_refuerzo,
      meses_refuerzo: form.requiere_refuerzo && form.meses_refuerzo !== "" ? Number(form.meses_refuerzo) : null,
    };
    try {
      if (editandoId) await esquemaApi.actualizar(token, editandoId, datos);
      else await esquemaApi.crear(token, datos);
      setMensaje(editandoId ? "Esquema actualizado." : "Esquema creado.");
      cancelar();
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function editar(esq) {
    setError("");
    try {
      const x = await esquemaApi.obtener(token, esq.id); // datos frescos del servidor
      setEditandoId(x.id);
      setForm({ ...x, meses_refuerzo: x.meses_refuerzo ?? "" });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelar() {
    setEditandoId(null);
    setForm(VACIO);
  }

  async function eliminar(esq) {
    if (!window.confirm(`¿Eliminar el esquema de ${nombreVacuna(esq.vacuna_id)} para ${nombreGrupo(esq.grupo_edad_id)}?`)) return;
    setError("");
    setMensaje("");
    try {
      await esquemaApi.eliminar(token, esq.id);
      setMensaje("Esquema eliminado.");
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Esquemas de vacunación</h1>
        <p>Dosis requeridas, intervalo entre dosis y refuerzo de cada vacuna según el grupo de edad.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {esAdmin && (
        <form className="tarjeta form-grid" onSubmit={guardar}>
          <h2>{editandoId ? "Editar esquema" : "Nuevo esquema"}</h2>
          <label>
            Vacuna
            <select value={form.vacuna_id} onChange={(e) => setForm((f) => ({ ...f, vacuna_id: e.target.value, grupo_edad_id: "" }))} required>
              <option value="">Seleccione…</option>
              {vacunas.map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
            </select>
          </label>
          <label>
            Grupo de edad
            <select value={form.grupo_edad_id} onChange={(e) => set("grupo_edad_id", e.target.value)} required>
              <option value="">Seleccione…</option>
              {gruposPosibles.map((g) => <option key={g.id} value={g.id}>{g.nombre} ({g.edad_min}–{g.edad_max} años)</option>)}
            </select>
          </label>
          <label>
            Cantidad de dosis
            <input type="number" min="1" value={form.cantidad_dosis} onChange={(e) => set("cantidad_dosis", e.target.value)} required />
          </label>
          <label>
            Días entre dosis
            <input type="number" min="0" value={form.dias_entre_dosis} onChange={(e) => set("dias_entre_dosis", e.target.value)} required />
          </label>
          <label>
            ¿Requiere refuerzo?
            <select value={form.requiere_refuerzo ? "si" : "no"} onChange={(e) => set("requiere_refuerzo", e.target.value === "si")}>
              <option value="no">No</option>
              <option value="si">Sí</option>
            </select>
          </label>
          {form.requiere_refuerzo && (
            <label>
              Meses hasta el refuerzo
              <input type="number" min="0" value={form.meses_refuerzo} onChange={(e) => set("meses_refuerzo", e.target.value)} required />
            </label>
          )}
          <div className="acciones ancho">
            <button className="btn" type="submit">{editandoId ? "Guardar cambios" : "Crear esquema"}</button>
            {editandoId && <button className="btn sec" type="button" onClick={cancelar}>Cancelar</button>}
          </div>
        </form>
      )}

      <section className="tarjeta">
        <h2>Esquemas registrados</h2>
        {cargando ? <p>Cargando…</p> : esquemas.length === 0 ? <p className="vacio">Aún no hay esquemas definidos.</p> : (
          <div className="scroll-x">
            <table className="tabla">
              <thead>
                <tr><th>Vacuna</th><th>Grupo de edad</th><th>Dosis</th><th>Días entre dosis</th><th>Refuerzo</th>{esAdmin && <th />}</tr>
              </thead>
              <tbody>
                {esquemas.map((x) => (
                  <tr key={x.id}>
                    <td>{nombreVacuna(x.vacuna_id)}</td>
                    <td><span className="badge suave">{nombreGrupo(x.grupo_edad_id)}</span></td>
                    <td>{x.cantidad_dosis}</td>
                    <td>{x.dias_entre_dosis}</td>
                    <td>{x.requiere_refuerzo ? <span className="badge pend">A los {x.meses_refuerzo ?? "—"} meses</span> : "—"}</td>
                    {esAdmin && (
                      <td className="celda-acc">
                        <button className="icon-btn" title="Editar" onClick={() => editar(x)}><Icon name="edit" size={18} /></button>
                        <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminar(x)}><Icon name="trash" size={18} /></button>
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
