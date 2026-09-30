import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { loteApi, movimientoApi, puntoApi, vacunaApi } from "../api/client.js";
import { Icon } from "../components/Icons.jsx";

const hoyISO = () => new Date().toISOString().slice(0, 10);
const fmt = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });
const fmtHora = (iso) => new Date(iso).toLocaleString("es-BO", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });

const ENTRADA_VACIA = { vacuna_id: "", numero_lote: "", fecha_fabricacion: hoyISO(), fecha_vencimiento: "", cantidad_inicial: "", umbral_minimo: 20 };
const SALIDA_VACIA = { lote_id: "", punto_id: "", cantidad: "" };
const AJUSTE_VACIO = { lote_id: "", tipo_movimiento: "salida", cantidad: "", observacion: "" };

export default function Stock() {
  const { token, esAdmin } = useAuth();
  const [d, setD] = useState({ lotes: [], stock: [], almacen: [], vacunas: [], puntos: [], movimientos: [], bajo: [], vencidos: [], sinStock: [] });
  const [filtroPunto, setFiltroPunto] = useState("");
  const [revision, setRevision] = useState(null);
  const [loteDetalle, setLoteDetalle] = useState(null);
  const [movDetalle, setMovDetalle] = useState(null);
  const [entrada, setEntrada] = useState(ENTRADA_VACIA);
  const [salida, setSalida] = useState(SALIDA_VACIA);
  const [ajuste, setAjuste] = useState(AJUSTE_VACIO);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = () => setVersion((v) => v + 1);

  useEffect(() => {
    let vivo = true;
    Promise.all([
      loteApi.listar(token),
      loteApi.stockPorPunto(token, filtroPunto),
      loteApi.almacenCentral(token),
      vacunaApi.listar(token),
      puntoApi.listar(token),
      movimientoApi.listar(token),
      loteApi.stockBajo(token),
      loteApi.vencidos(token),
      loteApi.puntosSinStock(token),
    ])
      .then(([lotes, stock, almacen, vacunas, puntos, movimientos, bajo, vencidos, sinStock]) => {
        if (!vivo) return;
        setD({ lotes, stock, almacen, vacunas, puntos, movimientos, bajo, vencidos, sinStock });
        setError("");
      })
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version, filtroPunto]);

  const vacuna = (id) => (id == null ? "—" : d.vacunas.find((v) => v.id === id)?.nombre ?? `#${id}`);
  const punto = (id) => (id == null ? "Almacén central" : d.puntos.find((p) => p.id === id)?.nombre ?? `#${id}`);
  const lote = (id) => d.lotes.find((l) => l.id === id);
  const lotesAlmacen = d.almacen.filter((l) => l.cantidad_actual > 0 && l.fecha_vencimiento >= hoyISO());
  const puntosActivos = d.puntos.filter((p) => p.estado === "activo");
  const loteSalida = lote(Number(salida.lote_id));

  async function ejecutar(accion, textoOk) {
    setError("");
    setMensaje("");
    try {
      await accion();
      setMensaje(textoOk);
      recargar();
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    }
  }

  async function enviarEntrada(e) {
    e.preventDefault();
    const ok = await ejecutar(
      () => loteApi.registrarEntrada(token, {
        ...entrada,
        vacuna_id: Number(entrada.vacuna_id),
        cantidad_inicial: Number(entrada.cantidad_inicial),
        umbral_minimo: Number(entrada.umbral_minimo),
      }),
      "Lote recibido en el almacén central."
    );
    if (ok) setEntrada(ENTRADA_VACIA);
  }

  async function enviarSalida(e) {
    e.preventDefault();
    const ok = await ejecutar(
      () => loteApi.registrarSalida(token, { lote_id: Number(salida.lote_id), punto_id: Number(salida.punto_id), cantidad: Number(salida.cantidad) }),
      "Dosis despachadas al punto."
    );
    if (ok) setSalida(SALIDA_VACIA);
  }

  async function enviarAjuste(e) {
    e.preventDefault();
    const ok = await ejecutar(
      () => movimientoApi.ajustar(token, {
        lote_id: Number(ajuste.lote_id),
        tipo_movimiento: ajuste.tipo_movimiento,
        cantidad: Number(ajuste.cantidad),
        observacion: ajuste.observacion || null,
      }),
      "Ajuste registrado."
    );
    if (ok) setAjuste(AJUSTE_VACIO);
  }

  async function revisarInventario() {
    setError("");
    setMensaje("");
    try {
      setRevision(await loteApi.revisionPeriodica(token));
      recargar();
    } catch (e) {
      setError(e.message);
    }
  }

  async function verLote(l) {
    setError("");
    try {
      setLoteDetalle(await loteApi.obtener(token, l.id));
    } catch (e) {
      setError(e.message);
    }
  }

  async function verMovimiento(m) {
    setError("");
    try {
      setMovDetalle(await movimientoApi.obtener(token, m.id));
    } catch (e) {
      setError(e.message);
    }
  }

  async function eliminarMovimiento(m) {
    if (!window.confirm("¿Eliminar este movimiento del historial?")) return;
    if (movDetalle?.id === m.id) setMovDetalle(null);
    ejecutar(() => movimientoApi.eliminar(token, m.id), "Movimiento eliminado.");
  }

  async function eliminarLote(l) {
    if (!window.confirm(`¿Eliminar el lote ${l.numero_lote}?`)) return;
    ejecutar(() => loteApi.eliminar(token, l.id), "Lote eliminado.");
  }

  const hoy = hoyISO();
  const alertas = d.bajo.length + d.vencidos.length + d.sinStock.length;

  return (
    <>
      <div className="encabezado">
        <h1>Stock de dosis</h1>
        <p>Recepción de lotes en el almacén central, despacho a los puntos y control de inventario.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      <div className="acciones">
        <button className="btn sec" onClick={revisarInventario}>Ejecutar revisión periódica de inventario</button>
      </div>

      {revision && (
        <section className="tarjeta">
          <div className="fila-titulo">
            <h2><Icon name="list" /> Resultado de la revisión periódica</h2>
            <button className="btn sec pequeno" onClick={() => setRevision(null)}>Cerrar</button>
          </div>
          {revision.lotes_con_stock_bajo.length === 0 && revision.lotes_vencidos.length === 0 && <p className="vacio">Sin novedades: no hay lotes con stock bajo ni vencidos.</p>}
          {revision.lotes_con_stock_bajo.map((l) => <p key={`rb${l.id}`} className="aviso">Stock bajo: lote {l.numero_lote} de {vacuna(l.vacuna_id)} en {punto(l.punto_id)} ({l.cantidad_actual} dosis, mínimo {l.umbral_minimo}).</p>)}
          {revision.lotes_vencidos.map((l) => <p key={`rv${l.id}`} className="aviso">Vencido: lote {l.numero_lote} de {vacuna(l.vacuna_id)} venció el {fmt(l.fecha_vencimiento)} ({l.cantidad_actual} dosis).</p>)}
        </section>
      )}

      {alertas > 0 && (
        <section className="tarjeta">
          <h2><Icon name="bell" /> Alertas de inventario</h2>
          {d.bajo.map((l) => <p key={`b${l.id}`} className="aviso">Stock bajo: lote {l.numero_lote} de {vacuna(l.vacuna_id)} en {punto(l.punto_id)} ({l.cantidad_actual} dosis, mínimo {l.umbral_minimo}).</p>)}
          {d.vencidos.map((l) => <p key={`v${l.id}`} className="aviso">Vencido: lote {l.numero_lote} de {vacuna(l.vacuna_id)} venció el {fmt(l.fecha_vencimiento)} ({l.cantidad_actual} dosis).</p>)}
          {d.sinStock.map((p) => <p key={`s${p.id}`} className="aviso">Sin stock: {p.nombre} no tiene dosis disponibles.</p>)}
        </section>
      )}

      <div className="rejilla">
        <form className="tarjeta form-grid" onSubmit={enviarEntrada}>
          <h2><Icon name="plus" /> Recibir lote (almacén central)</h2>
          <label className="ancho">
            Vacuna
            <select value={entrada.vacuna_id} onChange={(e) => setEntrada({ ...entrada, vacuna_id: e.target.value })} required>
              <option value="">Selecciona…</option>
              {d.vacunas.filter((v) => v.estado === "activa").map((v) => <option key={v.id} value={v.id}>{v.nombre}</option>)}
            </select>
          </label>
          <label>
            N.º de lote
            <input value={entrada.numero_lote} onChange={(e) => setEntrada({ ...entrada, numero_lote: e.target.value })} maxLength={50} required />
          </label>
          <label>
            Cantidad de dosis
            <input type="number" min="1" value={entrada.cantidad_inicial} onChange={(e) => setEntrada({ ...entrada, cantidad_inicial: e.target.value })} required />
          </label>
          <label>
            Fabricación
            <input type="date" value={entrada.fecha_fabricacion} onChange={(e) => setEntrada({ ...entrada, fecha_fabricacion: e.target.value })} required />
          </label>
          <label>
            Vencimiento
            <input type="date" value={entrada.fecha_vencimiento} onChange={(e) => setEntrada({ ...entrada, fecha_vencimiento: e.target.value })} required />
          </label>
          <label>
            Umbral mínimo
            <input type="number" min="0" value={entrada.umbral_minimo} onChange={(e) => setEntrada({ ...entrada, umbral_minimo: e.target.value })} required />
          </label>
          <div className="acciones ancho"><button className="btn" type="submit">Registrar entrada</button></div>
        </form>

        <form className="tarjeta form-grid" onSubmit={enviarSalida}>
          <h2><Icon name="syringe" /> Despachar a un punto</h2>
          <label className="ancho">
            Lote del almacén central
            <select value={salida.lote_id} onChange={(e) => setSalida({ ...salida, lote_id: e.target.value })} required>
              <option value="">Selecciona…</option>
              {lotesAlmacen.map((l) => <option key={l.id} value={l.id}>{vacuna(l.vacuna_id)} · lote {l.numero_lote} ({l.cantidad_actual} dosis)</option>)}
            </select>
          </label>
          <label>
            Punto de destino
            <select value={salida.punto_id} onChange={(e) => setSalida({ ...salida, punto_id: e.target.value })} required>
              <option value="">Selecciona…</option>
              {puntosActivos.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
            </select>
          </label>
          <label>
            Cantidad{loteSalida ? ` (máx. ${loteSalida.cantidad_actual})` : ""}
            <input type="number" min="1" max={loteSalida?.cantidad_actual} value={salida.cantidad} onChange={(e) => setSalida({ ...salida, cantidad: e.target.value })} required />
          </label>
          <div className="acciones ancho"><button className="btn" type="submit">Registrar salida</button></div>
          {lotesAlmacen.length === 0 && !cargando && <p className="vacio ancho">No hay lotes vigentes en el almacén central.</p>}
        </form>
      </div>

      <section className="tarjeta">
        <div className="fila-titulo">
          <h2>Lotes</h2>
          <select value={filtroPunto} onChange={(e) => setFiltroPunto(e.target.value)}>
            <option value="">Todas las ubicaciones</option>
            {d.puntos.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
        </div>
        {cargando ? <p>Cargando…</p> : d.stock.length === 0 ? <p className="vacio">Aún no hay lotes registrados.</p> : (
          <div className="scroll-x">
            <table className="tabla compacta">
              <thead><tr><th>Ubicación</th><th>Vacuna</th><th>Lote</th><th>Vence</th><th>Dosis</th><th>Estado</th><th /></tr></thead>
              <tbody>
                {[...d.stock].sort((a, b) => a.fecha_vencimiento.localeCompare(b.fecha_vencimiento)).map((l) => (
                  <tr key={l.id}>
                    <td>{punto(l.punto_id)}</td>
                    <td>{vacuna(l.vacuna_id)}</td>
                    <td>{l.numero_lote}</td>
                    <td>{fmt(l.fecha_vencimiento)}</td>
                    <td>{l.cantidad_actual} / {l.cantidad_inicial}</td>
                    <td>
                      {l.fecha_vencimiento < hoy ? <span className="badge pend">Vencido</span>
                        : l.stock_bajo ? <span className="badge pend">Stock bajo</span>
                        : <span className="badge ok">Vigente</span>}
                    </td>
                    <td className="celda-acc">
                      <button className="btn sec pequeno" onClick={() => verLote(l)}>Detalle</button>
                      {esAdmin && <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminarLote(l)}><Icon name="trash" size={18} /></button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {loteDetalle && (
        <section className="tarjeta">
          <div className="fila-titulo">
            <h2><Icon name="box" /> Lote {loteDetalle.numero_lote}</h2>
            <button className="btn sec pequeno" onClick={() => setLoteDetalle(null)}>Cerrar</button>
          </div>
          <ul className="lista-reg">
            <li><Icon name="syringe" /><div><strong>{vacuna(loteDetalle.vacuna_id)}</strong><small>{punto(loteDetalle.punto_id)}</small></div></li>
            <li><Icon name="calendar" /><div><strong>Fabricación {fmt(loteDetalle.fecha_fabricacion)}</strong><small>Vence {fmt(loteDetalle.fecha_vencimiento)}</small></div></li>
            <li><Icon name="box" /><div><strong>{loteDetalle.cantidad_actual} de {loteDetalle.cantidad_inicial} dosis</strong><small>Umbral mínimo {loteDetalle.umbral_minimo}{loteDetalle.stock_bajo ? " · stock bajo" : ""}</small></div></li>
          </ul>
        </section>
      )}

      <div className="rejilla">
        <form className="tarjeta form-grid" onSubmit={enviarAjuste}>
          <h2>Ajuste manual (merma, descarte, corrección)</h2>
          <label className="ancho">
            Lote
            <select value={ajuste.lote_id} onChange={(e) => setAjuste({ ...ajuste, lote_id: e.target.value })} required>
              <option value="">Selecciona…</option>
              {d.lotes.map((l) => <option key={l.id} value={l.id}>{vacuna(l.vacuna_id)} · lote {l.numero_lote} · {punto(l.punto_id)} ({l.cantidad_actual})</option>)}
            </select>
          </label>
          <label>
            Tipo
            <select value={ajuste.tipo_movimiento} onChange={(e) => setAjuste({ ...ajuste, tipo_movimiento: e.target.value })}>
              <option value="salida">Salida (resta)</option>
              <option value="entrada">Entrada (suma, solo almacén)</option>
            </select>
          </label>
          <label>
            Cantidad
            <input type="number" min="1" value={ajuste.cantidad} onChange={(e) => setAjuste({ ...ajuste, cantidad: e.target.value })} required />
          </label>
          <label className="ancho">
            Observación
            <input value={ajuste.observacion} onChange={(e) => setAjuste({ ...ajuste, observacion: e.target.value })} placeholder="Ej. frasco roto" />
          </label>
          <div className="acciones ancho"><button className="btn" type="submit">Registrar ajuste</button></div>
        </form>

        <section className="tarjeta">
          <h2>Últimos movimientos</h2>
          {d.movimientos.length === 0 ? <p className="vacio">Sin movimientos todavía.</p> : (
            <ul className="lista-reg">
              {[...d.movimientos].sort((a, b) => b.fecha_movimiento.localeCompare(a.fecha_movimiento)).slice(0, 8).map((m) => (
                <li key={m.id}>
                  <Icon name={m.tipo_movimiento === "entrada" ? "plus" : "syringe"} />
                  <div>
                    <strong>{m.tipo_movimiento === "entrada" ? "+" : "−"}{m.cantidad} · {vacuna(lote(m.lote_id)?.vacuna_id)}</strong>
                    <small>Lote {lote(m.lote_id)?.numero_lote ?? `#${m.lote_id}`}{m.punto_id ? ` → ${punto(m.punto_id)}` : ""} · {fmtHora(m.fecha_movimiento)}{m.observacion ? ` · ${m.observacion}` : ""}</small>
                  </div>
                  <button className="btn sec pequeno" onClick={() => verMovimiento(m)}>Detalle</button>
                  {esAdmin && <button className="icon-btn peligro" title="Eliminar" onClick={() => eliminarMovimiento(m)}><Icon name="trash" size={18} /></button>}
                </li>
              ))}
            </ul>
          )}
          {movDetalle && (
            <p className="aviso">
              Movimiento #{movDetalle.id}: {movDetalle.tipo_movimiento} de {movDetalle.cantidad} dosis · lote {lote(movDetalle.lote_id)?.numero_lote ?? `#${movDetalle.lote_id}`}
              {movDetalle.punto_id ? ` → ${punto(movDetalle.punto_id)}` : ""} · {fmtHora(movDetalle.fecha_movimiento)}
              {movDetalle.usuario_id ? ` · usuario #${movDetalle.usuario_id}` : ""}{movDetalle.observacion ? ` · ${movDetalle.observacion}` : ""}
              <button className="x" title="Cerrar" onClick={() => setMovDetalle(null)}>×</button>
            </p>
          )}
        </section>
      </div>
    </>
  );
}
