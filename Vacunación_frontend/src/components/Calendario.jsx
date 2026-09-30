import { useState } from "react";
import { Icon } from "./Icons.jsx";

const MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
const DIAS = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"];

const clave = (y, m, d) => `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;

// `marcados`: fechas "YYYY-MM-DD" con algún evento (inicio/fin de campaña)
export default function Calendario({ marcados = [] }) {
  const hoy = new Date();
  const [vista, setVista] = useState({ y: hoy.getFullYear(), m: hoy.getMonth() });
  const set = new Set(marcados);

  const primero = (new Date(vista.y, vista.m, 1).getDay() + 6) % 7; // lunes = 0
  const total = new Date(vista.y, vista.m + 1, 0).getDate();
  const celdas = [...Array(primero).fill(null), ...Array.from({ length: total }, (_, i) => i + 1)];

  function mover(delta) {
    const f = new Date(vista.y, vista.m + delta, 1);
    setVista({ y: f.getFullYear(), m: f.getMonth() });
  }

  return (
    <div className="cal">
      <div className="cal-nav">
        <button className="icon-btn" onClick={() => mover(-1)} aria-label="Mes anterior">
          <Icon name="left" size={18} />
        </button>
        <strong>{MESES[vista.m]} {vista.y}</strong>
        <button className="icon-btn" onClick={() => mover(1)} aria-label="Mes siguiente">
          <Icon name="chevron" size={18} />
        </button>
      </div>
      <div className="cal-grid">
        {DIAS.map((d) => <span key={d} className="cal-dia">{d}</span>)}
        {celdas.map((d, i) => {
          if (!d) return <span key={`v${i}`} />;
          const esHoy = d === hoy.getDate() && vista.m === hoy.getMonth() && vista.y === hoy.getFullYear();
          const marcado = set.has(clave(vista.y, vista.m, d));
          return (
            <span key={d} className={`cal-num ${esHoy ? "hoy" : ""} ${marcado ? "marca" : ""}`}>{d}</span>
          );
        })}
      </div>
    </div>
  );
}
