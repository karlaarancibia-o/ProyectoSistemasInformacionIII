import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { campanaApi, grupoEdadApi, puntoApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const VACIO = { nombre: "", tipo_temporada: "", fecha_inicio: "", fecha_fin: "", vacuna_id: "", descripcion: "", grupo_edad_ids: [] };
const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });
const claseEstado = { activa: "ok", planificada: "pend", finalizada: "off" };

export default function Campanas() {
  const { token, esAdmin } = useAuth();
  const [campanas, setCampanas] = useState([]);
  const [vacunas, setVacunas] = useState([]);
  const [grupos, setGrupos] = useState([]);
  const [puntos, setPuntos] = useState([]);
  const [form, setForm] = useState(VACIO);
  const [version, setVersion] = useState(0);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [soloActivas, setSoloActivas] = useState(false);

  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([soloActivas ? campanaApi.activas(token) : campanaApi.listar(token), vacunaApi.listar(token), grupoEdadApi.listar(token), puntoApi.listar(token)])
      .then(([c, v, g, p]) => {
        if (!vivo) return;
        setCampanas([...c].sort((a, b) => b.fecha_inicio.localeCompare(a.fecha_inicio)));
        setVacunas(v);
        setGrupos(g);
        setPuntos(p);
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version, soloActivas]);

  const vacunaSel = vacunas.find((v) => v.id === Number(form.vacuna_id));
  const gruposDeVacuna = grupos.filter((g) => vacunaSel?.grupo_edad_ids?.includes(g.id));
  const nombreVacuna = (id) => vacunas.find((v) => v.id === id)?.nombre ?? `#${id}`;
  const nombreGrupo = (id) => grupos.find((g) => g.id === id)?.nombre ?? `#${id}`;
  const nombrePunto = (id) => puntos.find((p) => p.id === id)?.nombre ?? `#${id}`;

  const set = (campo, valor) => setForm((f) => ({ ...f, [campo]: valor }));

  function alternarGrupo(id) {
    setForm((f) => ({
      ...f,
      grupo_edad_ids: f.grupo_edad_ids.includes(id) ? f.grupo_edad_ids.filter((x) => x !== id) : [...f.grupo_edad_ids, id],
    }));
  }

  async function accion(fn, textoOk) {
    setError("");
    setMensaje("");
    try {
      await fn();
      if (textoOk) setMensaje(textoOk);
      recargar();
    } catch (e) {
      setError(e.message);
    }
  }

  async function crear(e) {
    e.preventDefault();
    await accion(async () => {
      await campanaApi.crear(token, { ...form, vacuna_id: Number(form.vacuna_id), descripcion: form.descripcion || null });
      setForm(VACIO);
    }, "Campaña creada (queda planificada hasta su fecha de inicio).");
  }

  return (
    <>
      <div className="encabezado">
        <h1>Campañas</h1>
        <p>Campañas de vacunación estacionales, sus grupos de edad y puntos de vacunación.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {esAdmin && (
        <form className="tarjeta form-grid" onSubmit={crear}>
          <h2>Nueva campaña</h2>
          <label>Nombre<input value={form.nombre} onChange={(e) => set("nombre", e.target.value)} minLength={2} required /></label>
          <label>Temporada<input value={form.tipo_temporada} onChange={(e) => set("tipo_temporada", e.target.value)} placeholder="Ej. Influenza estacional" minLength={2} required /></label>
          <label>Inicio<input type="date" value={form.fecha_inicio} onChange={(e) => set("fecha_inicio", e.target.value)} required /></label>
          <label>Fin<input type="date" value={form.fecha_fin} onChange={(e) => set("fecha_fin", e.target.value)} required /></label>
          <label>
            Vacuna
            <select value={form.vacuna_id} onChange={(e) => setForm((f) => ({ ...f, vacuna_id: e.target.value, grupo_edad_ids: [] }))} required>
              <option value="">Seleccione…</option>
              {vacunas.filter((v) => v.estado === "activa").map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
            </select>
          </label>
          <label className="ancho">Descripción<input value={form.descripcion} onChange={(e) => set("descripcion", e.target.value)} /></label>

          <fieldset className="ancho grupos-sel">
            <legend>Grupos de edad objetivo (opcional)</legend>
            {!vacunaSel ? (
              <p className="vacio">Elija una vacuna para ver los grupos a los que está indicada.</p>
            ) : gruposDeVacuna.length === 0 ? (
              <p className="vacio">Esta vacuna aún no tiene grupos de edad.</p>
            ) : (
              <div className="chips">
                {gruposDeVacuna.map((g) => {
                  const on = form.grupo_edad_ids.includes(g.id);
                  return (
                    <label key={g.id} className={`chip ${on ? "on" : ""}`}>
                      <input type="checkbox" checked={on} onChange={() => alternarGrupo(g.id)} />
                      {on && <Icon name="check" size={14} />}{g.nombre} <small>({g.edad_min}–{g.edad_max} años)</small>
                    </label>
                  );
                })}
              </div>
            )}
          </fieldset>

          <div className="acciones ancho"><button className="btn" type="submit">Crear campaña</button></div>
        </form>
      )}

      {esAdmin && (
        <div className="acciones">
          <button className="btn sec" onClick={() => accion(() => campanaApi.activarProgramadas(token), "Campañas programadas activadas.")}>Activar programadas</button>
          <button className="btn sec" onClick={() => accion(() => campanaApi.finalizarVencidas(token), "Campañas vencidas finalizadas.")}>Finalizar vencidas</button>
        </div>
      )}

      <label className="chip-check">
        <input type="checkbox" checked={soloActivas} onChange={(e) => setSoloActivas(e.target.checked)} /> Mostrar solo campañas activas
      </label>

      {cargando ? <p>Cargando…</p> : campanas.length === 0 ? (
        <p className="tarjeta vacio">Aún no hay campañas.</p>
      ) : (
        campanas.map((c) => {
          const libres = puntos.filter((p) => !c.punto_ids.includes(p.id));
          const gruposVacuna = vacunas.find((v) => v.id === c.vacuna_id)?.grupo_edad_ids ?? [];
          const gruposLibres = grupos.filter((g) => gruposVacuna.includes(g.id) && !c.grupo_edad_ids.includes(g.id));
          return (
            <section key={c.id} className="tarjeta campana">
              <div className="campana-cab">
                <div>
                  <h2>{c.nombre}</h2>
                  <small>{c.tipo_temporada} · {nombreVacuna(c.vacuna_id)} · {fmt(c.fecha_inicio)} → {fmt(c.fecha_fin)}</small>
                </div>
                <span className={`badge ${claseEstado[c.estado]}`}>{c.estado}</span>
                {esAdmin && (
                  <button className="icon-btn peligro" title="Eliminar" onClick={() => window.confirm(`¿Eliminar "${c.nombre}"?`) && accion(() => campanaApi.eliminar(token, c.id), "Campaña eliminada.")}>
                    <Icon name="trash" size={18} />
                  </button>
                )}
              </div>
              {c.descripcion && <p className="vacio">{c.descripcion}</p>}
              <p>
                <strong>Grupos de edad:</strong>{" "}
                {c.grupo_edad_ids.length === 0 && "Todos los de la vacuna"}
                {c.grupo_edad_ids.map((id) => (
                  <span key={id} className="badge suave">
                    {nombreGrupo(id)}
                    {esAdmin && <button className="x" title="Quitar" onClick={() => accion(() => campanaApi.quitarGrupo(token, c.id, id))}>×</button>}
                  </span>
                ))}
              </p>
              {esAdmin && gruposLibres.length > 0 && (
                <select className="sel-punto" value="" onChange={(e) => e.target.value && accion(() => campanaApi.asignarGrupo(token, c.id, Number(e.target.value)))}>
                  <option value="">+ Asignar grupo de edad…</option>
                  {gruposLibres.map((g) => <option key={g.id} value={g.id}>{g.nombre}</option>)}
                </select>
              )}
              <p>
                <strong>Puntos de vacunación:</strong>{" "}
                {c.punto_ids.length === 0 && "Ninguno asignado"}
                {c.punto_ids.map((id) => (
                  <span key={id} className="badge suave">
                    {nombrePunto(id)}
                    {esAdmin && <button className="x" title="Quitar" onClick={() => accion(() => campanaApi.quitarPunto(token, c.id, id))}>×</button>}
                  </span>
                ))}
              </p>
              {esAdmin && libres.length > 0 && (
                <select className="sel-punto" value="" onChange={(e) => e.target.value && accion(() => campanaApi.asignarPunto(token, c.id, Number(e.target.value)))}>
                  <option value="">+ Asignar punto…</option>
                  {libres.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                </select>
              )}
            </section>
          );
        })
      )}
    </>
  );
}
