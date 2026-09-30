import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { campanaApi, loteApi, pacienteApi, puntoApi, vacunaApi, vacunacionApi } from "../api/client.js";

const hoyISO = () => new Date().toISOString().slice(0, 10);

export default function RegistrarDosis() {
  const { token } = useAuth();
  const [datos, setDatos] = useState({ pacientes: [], campanas: [], puntos: [], lotes: [], vacunas: [] });
  const [form, setForm] = useState({ paciente_id: "", campana_id: "", punto_id: "", lote_id: "", fecha_aplicacion: hoyISO() });
  const [version, setVersion] = useState(0);
  const [cargando, setCargando] = useState(true);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    let vivo = true;
    Promise.all([pacienteApi.listar(token), campanaApi.listar(token), puntoApi.listar(token), loteApi.listar(token), vacunaApi.listar(token)])
      .then(([pacientes, campanas, puntos, lotes, vacunas]) => vivo && setDatos({ pacientes, campanas, puntos, lotes, vacunas }))
      .catch((e) => vivo && setError(e.message))
      .finally(() => vivo && setCargando(false));
    return () => {
      vivo = false;
    };
  }, [token, version]);

  const campanasActivas = datos.campanas.filter((c) => c.estado === "activa");
  const campana = campanasActivas.find((c) => c.id === Number(form.campana_id));
  const puntosCampana = datos.puntos.filter((p) => campana?.punto_ids.includes(p.id) && p.estado === "activo");
  const lotesDisponibles = datos.lotes.filter(
    (l) =>
      campana && l.vacuna_id === campana.vacuna_id && l.punto_id === Number(form.punto_id) &&
      l.cantidad_actual > 0 && l.fecha_vencimiento >= form.fecha_aplicacion
  );
  const nombreVacuna = datos.vacunas.find((v) => v.id === campana?.vacuna_id)?.nombre;

  const set = (c, v) => setForm((f) => ({ ...f, [c]: v }));

  async function enviar(e) {
    e.preventDefault();
    setError("");
    setMensaje("");
    setEnviando(true);
    try {
      const r = await vacunacionApi.registrarDosis(token, {
        paciente_id: Number(form.paciente_id),
        campana_id: Number(form.campana_id),
        punto_id: Number(form.punto_id),
        lote_id: Number(form.lote_id),
        fecha_aplicacion: form.fecha_aplicacion,
      });
      setMensaje(`Dosis registrada: ${r.es_refuerzo ? "refuerzo" : `dosis ${r.numero_dosis}`} de ${nombreVacuna}.`);
      setForm((f) => ({ ...f, paciente_id: "", lote_id: "" }));
      setVersion((v) => v + 1);
    } catch (err) {
      setError(err.message); // el backend explica por qué no corresponde (edad, intervalo, stock…)
    } finally {
      setEnviando(false);
    }
  }

  return (
    <>
      <div className="encabezado">
        <h1>Registrar dosis</h1>
        <p>El sistema calcula el número de dosis y valida edad, intervalo, stock y vigencia del lote.</p>
      </div>

      {error && <p className="msg error">{error}</p>}
      {mensaje && <p className="msg ok">{mensaje}</p>}

      {cargando ? <p>Cargando…</p> : (
        <form className="tarjeta form-grid" onSubmit={enviar}>
          <label className="ancho">
            Paciente
            <select value={form.paciente_id} onChange={(e) => set("paciente_id", e.target.value)} required>
              <option value="">Seleccione…</option>
              {datos.pacientes.map((p) => <option key={p.id} value={p.id}>{p.nombres} {p.apellidos} — CI {p.carnet_identidad}</option>)}
            </select>
          </label>
          <label>
            Campaña activa
            <select value={form.campana_id} onChange={(e) => setForm((f) => ({ ...f, campana_id: e.target.value, punto_id: "", lote_id: "" }))} required>
              <option value="">{campanasActivas.length ? "Seleccione…" : "No hay campañas activas"}</option>
              {campanasActivas.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
            </select>
          </label>
          <label>
            Punto de vacunación
            <select value={form.punto_id} onChange={(e) => setForm((f) => ({ ...f, punto_id: e.target.value, lote_id: "" }))} required disabled={!campana}>
              <option value="">{campana && puntosCampana.length === 0 ? "La campaña no tiene puntos activos" : "Seleccione…"}</option>
              {puntosCampana.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
            </select>
          </label>
          <label>
            Lote {nombreVacuna && <small>({nombreVacuna})</small>}
            <select value={form.lote_id} onChange={(e) => set("lote_id", e.target.value)} required disabled={!form.punto_id}>
              <option value="">{form.punto_id && lotesDisponibles.length === 0 ? "Sin lotes con dosis en este punto" : "Seleccione…"}</option>
              {lotesDisponibles.map((l) => <option key={l.id} value={l.id}>{l.numero_lote} · {l.cantidad_actual} dosis · vence {l.fecha_vencimiento}</option>)}
            </select>
          </label>
          <label>
            Fecha de aplicación
            <input type="date" max={hoyISO()} value={form.fecha_aplicacion} onChange={(e) => set("fecha_aplicacion", e.target.value)} required />
          </label>
          <div className="acciones ancho">
            <button className="btn" type="submit" disabled={enviando}>{enviando ? "Registrando…" : "Registrar dosis"}</button>
          </div>
        </form>
      )}
    </>
  );
}
