import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { campanaApi, pacienteApi, vacunaApi, vacunacionApi } from "../api/client.js";
import { Icon, Logo } from "../components/Icons.jsx";
import Calendario from "../components/Calendario.jsx";

const fmt = (iso) =>
  new Date(iso + "T00:00:00").toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" });

const ok = (r) => (r.status === "fulfilled" ? r.value : null);

export default function Inicio() {
  const { token, usuario } = useAuth();
  const [d, setD] = useState({ pacientes: null, registros: null, campanas: null, pendientes: null, vacunas: [] });
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    let vivo = true;
    // cada rol ve solo lo que su permiso permite: los rechazados quedan en null
    Promise.allSettled([
      pacienteApi.listar(token),
      vacunacionApi.registros(token),
      campanaApi.listar(token),
      vacunaApi.listar(token),
    ]).then(async ([p, r, c, v]) => {
      const vacunas = ok(v) || [];
      // el backend calcula dosis pendientes por vacuna: se consulta cada una y se juntan
      const porVacuna = await Promise.allSettled(
        vacunas.map((x) => vacunacionApi.dosisPendientes(token, x.id))
      );
      const consultas = porVacuna.map(ok);
      const pendientes = vacunas.length === 0 ? [] : consultas.some((x) => x !== null) ? consultas.flatMap((x) => x || []) : null;
      if (!vivo) return;
      setD({ pacientes: ok(p), registros: ok(r), campanas: ok(c), pendientes, vacunas });
      setCargando(false);
    });
    return () => {
      vivo = false;
    };
  }, [token]);

  const hoy = new Date();
  const mesActual = `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, "0")}`;

  const s = useMemo(() => {
    const registros = d.registros || [];
    const campanas = d.campanas || [];
    const pend = d.pendientes || [];
    const aplicadas = pend.reduce((t, x) => t + x.esquema.dosis_aplicadas, 0);
    const requeridas = pend.reduce((t, x) => t + x.esquema.dosis_requeridas, 0);
    return {
      delMes: registros.filter((r) => r.fecha_aplicacion.startsWith(mesActual)).length,
      activas: campanas.filter((c) => c.estado === "activa").length,
      pendientes: new Set(pend.filter((x) => x.esquema.dosis_pendientes > 0).map((x) => x.paciente_id)).size,
      cobertura: requeridas ? Math.round((aplicadas / requeridas) * 100) : null,
      ultimos: [...registros].sort((a, b) => b.fecha_aplicacion.localeCompare(a.fecha_aplicacion) || b.id - a.id).slice(0, 5),
      campanasOrden: [...campanas].sort((a, b) => a.fecha_inicio.localeCompare(b.fecha_inicio)).slice(-5).reverse(),
      marcados: campanas.flatMap((c) => [c.fecha_inicio, c.fecha_fin]),
    };
  }, [d, mesActual]);

  const nombreVacuna = (id) => d.vacunas.find((v) => v.id === id)?.nombre ?? `Vacuna #${id}`;
  const dato = (v, sufijo = "") => (v === null || v === undefined ? "—" : `${v}${sufijo}`);
  const cob = s.cobertura ?? 0;

  return (
    <>
      <div className="bienvenida">
        <div>
          <h1>Bienvenido, {usuario.username}</h1>
          <p>Aquí tienes un resumen de la actividad y las campañas de vacunación.</p>
        </div>
        <div className="banner-mini">
          <Logo size={54} color="#c1121f" />
          <div>
            <strong>Las vacunas protegen tu vida</strong>
            <small>Mantente al día con tu esquema de vacunación.</small>
          </div>
        </div>
      </div>

      <div className="stats">
        <Stat icon="users" titulo="Pacientes registrados" valor={dato(d.pacientes?.length)} pie="Personas registradas" />
        <Stat icon="syringe" titulo="Dosis aplicadas" valor={dato(d.registros ? s.delMes : null)} pie="Este mes" />
        <Stat icon="megaphone" titulo="Campañas activas" valor={dato(d.campanas ? s.activas : null)} pie="En curso ahora" />
        <Stat icon="check" titulo="Cobertura" valor={dato(s.cobertura, "%")} pie="Dosis aplicadas vs. requeridas" />
      </div>

      <div className="rejilla">
        <section className="tarjeta ancha">
          <h2><Icon name="megaphone" /> Campañas</h2>
          {cargando ? <p>Cargando…</p> : !d.campanas ? <p className="vacio">Sin acceso a campañas.</p> : s.campanasOrden.length === 0 ? (
            <p className="vacio">No hay campañas registradas.</p>
          ) : (
            <table className="tabla compacta">
              <thead>
                <tr><th>Inicio</th><th>Campaña</th><th>Vacuna</th><th>Estado</th></tr>
              </thead>
              <tbody>
                {s.campanasOrden.map((c) => (
                  <tr key={c.id}>
                    <td>{fmt(c.fecha_inicio)}</td>
                    <td>{c.nombre}</td>
                    <td>{nombreVacuna(c.vacuna_id)}</td>
                    <td><span className={`badge ${c.estado === "activa" ? "ok" : c.estado === "planificada" ? "pend" : "off"}`}>{c.estado}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="tarjeta">
          <h2><Icon name="calendar" /> Calendario</h2>
          <Calendario marcados={s.marcados} />
          <p className="leyenda"><span className="punto" /> Inicio o fin de campaña</p>
        </section>

        <section className="tarjeta">
          <h2><Icon name="list" /> Últimos registros</h2>
          {!d.registros ? <p className="vacio">Sin acceso a registros.</p> : s.ultimos.length === 0 ? (
            <p className="vacio">Aún no hay dosis registradas.</p>
          ) : (
            <ul className="lista-reg">
              {s.ultimos.map((r) => (
                <li key={r.id}>
                  <Icon name="syringe" />
                  <div>
                    <strong>{nombreVacuna(r.vacuna_id)}</strong>
                    <small>{fmt(r.fecha_aplicacion)} · dosis {r.numero_dosis}{r.es_refuerzo ? " (refuerzo)" : ""}</small>
                  </div>
                  <span className="badge ok">Aplicada</span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="tarjeta esquema ancha">
          <div className="esquema-cab">Cobertura del esquema de vacunación</div>
          <div className="esquema-cuerpo">
            <div className="donut" style={{ "--p": cob }}>
              <div><strong>{dato(s.cobertura, "%")}</strong><small>Completado</small></div>
            </div>
            <div>
              <h3>Pacientes con dosis pendientes</h3>
              <p className="grande">{dato(d.pendientes ? s.pendientes : null)}</p>
              <p className="aviso"><Icon name="bell" size={16} /> Contacta a los pacientes para completar su esquema.</p>
            </div>
          </div>
        </section>

        <section className="tarjeta">
          <h2>Información importante</h2>
          <ul className="info">
            <li><Icon name="calendar" /><div><strong>¿Qué vacunas corresponden?</strong><small>Según la edad, definida por grupo de edad.</small></div></li>
            <li><Icon name="bell" /><div><strong>Recomendaciones</strong><small>Cuidados antes y después de la vacunación.</small></div></li>
          </ul>
        </section>

        <section className="banner-grande">
          <Logo size={80} />
          <div>
            <h2>La prevención está en tus manos</h2>
            <p>Vacúnate hoy, protege tu mañana.</p>
          </div>
        </section>
      </div>
    </>
  );
}

function Stat({ icon, titulo, valor, pie }) {
  return (
    <div className="tarjeta stat">
      <div className="stat-ico"><Icon name={icon} size={28} /></div>
      <div>
        <small>{titulo}</small>
        <strong>{valor}</strong>
        <small>{pie}</small>
      </div>
    </div>
  );
}
