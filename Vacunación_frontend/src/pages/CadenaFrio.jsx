import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { loteApi, puntoApi, temperaturaApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const fmtHora = (iso) => new Date(iso).toLocaleString("es-BO", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
// valor para <input type="datetime-local"> en hora local
const ahoraLocal = () => {
  const n = new Date();
  n.setMinutes(n.getMinutes() - n.getTimezoneOffset());
  return n.toISOString().slice(0, 16);
};

export default function CadenaFrio() {
  const { token, esAdmin } = useAuth();
  const [d, setD] = useState({ puntos: [], vacunas: [], registros: [], fuera: [], pendientes: [] });
  const [form, setForm] = useState({ punto_id: "", vacuna_id: "", temperatura_celsius: "", fecha_hora: ahoraLocal(), observacion: "" });
  const [vacunasPunto, setVacunasPunto] = useState([]);
  const [filtroPunto, setFiltroPunto] = useState("");
  const [detalle, setDetalle] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([
      puntoApi.listar(token),
      vacunaApi.listar(token),
      temperaturaApi.listar(token, filtroPunto),
      temperaturaApi.fueraDeRango(token),
      temperaturaApi.puntosPendientes(token),
    ])
      .then(([puntos, vacunas, registros, fuera, pendientes]) => {
        if (!vivo) return;
        setD({ puntos, vacunas, registros, fuera, pendientes });
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version, filtroPunto]);

  // al elegir un punto, solo se ofrecen las vacunas que tienen stock allí
  useEffect(() => {
    if (!form.punto_id) return;
    let vivo = true;
    loteApi
      .vacunasEnPunto(token, form.punto_id)
      .then((v) => vivo && setVacunasPunto(v))
      .catch((e) => vivo && setError(e.message));
    return () => {
      vivo = false;
    };
  }, [token, form.punto_id]);

  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));
  const punto = (id) => d.puntos.find((p) => p.id === id)?.nombre ?? `#${id}`;
  const vacuna = (id) => d.vacunas.find((v) => v.id === id);
  const vacunaSel = vacuna(Number(form.vacuna_id));

  function elegirPunto(id) {
    setVacunasPunto([]);
    setForm((f) => ({ ...f, punto_id: id, vacuna_id: "" }));
  }

  async function enviar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    try {
      const r = await temperaturaApi.registrar(token, Number(form.punto_id), {
        vacuna_id: Number(form.vacuna_id),
        temperatura_celsius: Number(form.temperatura_celsius),
        fecha_hora: new Date(form.fecha_hora).toISOString(),
        observacion: form.observacion || null,
      });
      setMensaje(r.fuera_de_rango ? "Registrada: la temperatura está FUERA del rango de la vacuna." : "Temperatura registrada dentro del rango.");
      setForm((f) => ({ ...f, temperatura_celsius: "", fecha_hora: ahoraLocal(), observacion: "" }));
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  async function ver(r) {
    setError("");
    try {
      setDetalle(await temperaturaApi.obtener(token, r.id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function eliminar(r) {
    if (!window.confirm("¿Eliminar este registro de temperatura?")) return;
    try {
      await temperaturaApi.eliminar(token, r.id);
      recargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Cadena de frío</h1>
        <p>Registro de temperaturas por punto y vacuna, con alerta cuando salen del rango permitido.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {(d.fuera.length > 0 || d.pendientes.length > 0) && (
        <section className="tarjeta">
          <h2><Icon name="bell" /> Alertas</h2>
          {d.fuera.slice(0, 5).map((r) => (
            <p key={r.id} className="aviso">
              Fuera de rango: {r.temperatura_celsius} °C de {vacuna(r.vacuna_id)?.nombre ?? `#${r.vacuna_id}`} en {punto(r.punto_id)} ({fmtHora(r.fecha_hora)}).
            </p>
          ))}
          {d.pendientes.map((p) => <p key={p.id} className="aviso">Pendiente: {p.nombre} aún no registra temperatura hoy.</p>)}
        </section>
      )}

      <form className="tarjeta form-grid" onSubmit={enviar}>
        <h2><Icon name="plus" /> Registrar temperatura</h2>
        <label>
          Punto de vacunación
          <select value={form.punto_id} onChange={(e) => elegirPunto(e.target.value)} required>
            <option value="">Selecciona…</option>
            {d.puntos.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
        </label>
        <label>
          Vacuna (con stock en el punto)
          <select value={form.vacuna_id} onChange={(e) => set("vacuna_id", e.target.value)} disabled={!form.punto_id} required>
            <option value="">{form.punto_id && vacunasPunto.length === 0 ? "Sin vacunas con stock" : "Selecciona…"}</option>
            {vacunasPunto.map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
          </select>
        </label>
        <label>
          Temperatura (°C){vacunaSel ? ` — rango ${vacunaSel.temperatura_minima} a ${vacunaSel.temperatura_maxima}` : ""}
          <input type="number" step="0.1" value={form.temperatura_celsius} onChange={(e) => set("temperatura_celsius", e.target.value)} required />
        </label>
        <label>
          Fecha y hora
          <input type="datetime-local" value={form.fecha_hora} onChange={(e) => set("fecha_hora", e.target.value)} required />
        </label>
        <label className="ancho">
          Observación
          <input value={form.observacion} onChange={(e) => set("observacion", e.target.value)} />
        </label>
        <div className="acciones ancho"><button className="btn" type="submit">Registrar</button></div>
      </form>

      <section className="tarjeta">
        <div className="fila-titulo">
          <h2>Historial</h2>
          <select className="filtro" value={filtroPunto} onChange={(e) => setFiltroPunto(e.target.value)}>
            <option value="">Todos los puntos</option>
            {d.puntos.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
        </div>
        {cargando ? <p>Cargando…</p> : d.registros.length === 0 ? <p className="vacio">Sin registros de temperatura.</p> : (
          <div className="scroll-x">
            <table className="tabla compacta">
              <thead><tr><th>Fecha</th><th>Punto</th><th>Vacuna</th><th>Temperatura</th><th>Estado</th><th>Observación</th><th /></tr></thead>
              <tbody>
                {[...d.registros].sort((a, b) => b.fecha_hora.localeCompare(a.fecha_hora)).map((r) => (
                  <tr key={r.id}>
                    <td>{fmtHora(r.fecha_hora)}</td>
                    <td>{punto(r.punto_id)}</td>
                    <td>{vacuna(r.vacuna_id)?.nombre ?? `#${r.vacuna_id}`}</td>
                    <td>{r.temperatura_celsius} °C</td>
                    <td><span className={`badge ${r.fuera_de_rango ? "pend" : "ok"}`}>{r.fuera_de_rango ? "Fuera de rango" : "En rango"}</span></td>
                    <td>{r.observacion || "—"}</td>
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
            <h2><Icon name="snow" /> Registro de temperatura #{detalle.id}</h2>
            <button className="btn sec pequeno" onClick={() => setDetalle(null)}>Cerrar</button>
          </div>
          <ul className="lista-reg">
            <li><Icon name="pin" /><div><strong>{punto(detalle.punto_id)}</strong><small>{vacuna(detalle.vacuna_id)?.nombre ?? `#${detalle.vacuna_id}`} · rango {vacuna(detalle.vacuna_id) ? `${vacuna(detalle.vacuna_id).temperatura_minima} a ${vacuna(detalle.vacuna_id).temperatura_maxima} °C` : "—"}</small></div></li>
            <li><Icon name="snow" /><div><strong>{detalle.temperatura_celsius} °C</strong><small>{fmtHora(detalle.fecha_hora)}{detalle.usuario_id ? ` · registrado por usuario #${detalle.usuario_id}` : ""}</small></div><span className={`badge ${detalle.fuera_de_rango ? "pend" : "ok"}`}>{detalle.fuera_de_rango ? "Fuera de rango" : "En rango"}</span></li>
            {detalle.observacion && <li><Icon name="list" /><div><strong>Observación</strong><small>{detalle.observacion}</small></div></li>}
          </ul>
        </section>
      )}
    </>
  );
}
