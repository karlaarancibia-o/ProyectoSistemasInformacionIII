// Capa de acceso a la API (misma convención que el proyecto de ejemplo).
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path, { method = "GET", token, body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `Error ${res.status}` }));
    // FastAPI devuelve `detail` como texto (errores de dominio) o como lista (422 de validación)
    const detalle = Array.isArray(err.detail)
      ? err.detail.map((d) => d.msg).join(". ")
      : err.detail;
    const e = new Error(detalle || `Error ${res.status}`);
    e.status = res.status;
    throw e;
  }
  return res.status === 204 ? null : res.json();
}

export const authApi = {
  registrar: (username, password, rol, token) =>
    request("/auth/registro", { method: "POST", token, body: { username, password, ...(rol ? { rol } : {}) } }),

  login: async (username, password) => {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(typeof err.detail === "string" ? err.detail : "Credenciales inválidas");
    }
    return res.json();
  },

  me: (token) => request("/auth/me", { token }),
  roles: (token) => request("/auth/roles", { token }),
  usuarios: (token) => request("/auth/usuarios", { token }),
  cambiarRol: (token, id, rol) =>
    request(`/auth/usuarios/${id}/rol`, { method: "PATCH", token, body: { rol } }),
  cambiarEstado: (token, id, activo) =>
    request(`/auth/usuarios/${id}/estado`, { method: "PATCH", token, body: { activo } }),
};

export const grupoEdadApi = {
  listar: (token) => request("/grupos-edad/", { token }),
  crear: (token, datos) => request("/grupos-edad/", { method: "POST", token, body: datos }),
  actualizar: (token, id, datos) =>
    request(`/grupos-edad/${id}`, { method: "PUT", token, body: datos }),
  obtener: (token, id) => request(`/grupos-edad/${id}`, { token }),
  editarPrioridad: (token, id, nueva_prioridad) =>
    request(`/grupos-edad/${id}/prioridad`, { method: "PATCH", token, body: { nueva_prioridad } }),
  eliminar: (token, id) => request(`/grupos-edad/${id}`, { method: "DELETE", token }),
};

export const vacunaApi = {
  listar: (token) => request("/vacunas/", { token }),
  obtener: (token, id) => request(`/vacunas/${id}`, { token }),
  crear: (token, datos) => request("/vacunas/", { method: "POST", token, body: datos }),
  actualizar: (token, id, datos) =>
    request(`/vacunas/${id}`, { method: "PUT", token, body: datos }),
  eliminar: (token, id) => request(`/vacunas/${id}`, { method: "DELETE", token }),
};

export const campanaApi = {
  listar: (token) => request("/campanas/", { token }),
  activas: (token) => request("/campanas/activas", { token }),
  obtener: (token, id) => request(`/campanas/${id}`, { token }),
  asignarGrupo: (token, id, grupo_edad_id) =>
    request(`/campanas/${id}/asignar-grupo-edad`, { method: "POST", token, body: { grupo_edad_id } }),
  quitarGrupo: (token, id, grupoId) =>
    request(`/campanas/${id}/grupos-edad/${grupoId}`, { method: "DELETE", token }),
  crear: (token, datos) => request("/campanas/", { method: "POST", token, body: datos }),
  eliminar: (token, id) => request(`/campanas/${id}`, { method: "DELETE", token }),
  activarProgramadas: (token) =>
    request("/campanas/activar-programadas", { method: "POST", token }),
  finalizarVencidas: (token) =>
    request("/campanas/finalizar-vencidas", { method: "POST", token }),
  asignarPunto: (token, id, punto_id) =>
    request(`/campanas/${id}/asignar-punto`, { method: "POST", token, body: { punto_id } }),
  quitarPunto: (token, id, punto_id) =>
    request(`/campanas/${id}/puntos/${punto_id}`, { method: "DELETE", token }),
};

export const puntoApi = {
  listar: (token) => request("/puntos-vacunacion/", { token }),
  crear: (token, datos) => request("/puntos-vacunacion/", { method: "POST", token, body: datos }),
  actualizar: (token, id, datos) =>
    request(`/puntos-vacunacion/${id}`, { method: "PATCH", token, body: datos }),
  eliminar: (token, id) => request(`/puntos-vacunacion/${id}`, { method: "DELETE", token }),
  obtener: (token, id) => request(`/puntos-vacunacion/${id}`, { token }),
  sinStock: (token) => request("/puntos-vacunacion/sin-stock", { token }),
  temperaturasPendientes: (token) => request("/puntos-vacunacion/temperaturas-pendientes", { token }),
  horarios: (token, id) => request(`/puntos-vacunacion/${id}/horarios`, { token }),
  obtenerHorario: (token, id, horarioId) => request(`/puntos-vacunacion/${id}/horarios/${horarioId}`, { token }),
  actualizarHorario: (token, id, horarioId, datos) =>
    request(`/puntos-vacunacion/${id}/horarios/${horarioId}`, { method: "PATCH", token, body: datos }),
  definirHorario: (token, id, datos) =>
    request(`/puntos-vacunacion/${id}/horarios`, { method: "POST", token, body: datos }),
  eliminarHorario: (token, id, horarioId) =>
    request(`/puntos-vacunacion/${id}/horarios/${horarioId}`, { method: "DELETE", token }),
};

export const loteApi = {
  listar: (token) => request("/stock-dosis/lotes", { token }),
  obtener: (token, id) => request(`/stock-dosis/lotes/${id}`, { token }),
  stockPorPunto: (token, puntoId) => request(`/stock-dosis/${puntoId ? `?punto_id=${puntoId}` : ""}`, { token }),
  almacenCentral: (token) => request("/stock-dosis/almacen-central", { token }),
  revisionPeriodica: (token) => request("/stock-dosis/revision-periodica", { method: "POST", token }),
  eliminar: (token, id) => request(`/stock-dosis/lotes/${id}`, { method: "DELETE", token }),
  registrarEntrada: (token, datos) =>
    request("/stock-dosis/entradas", { method: "POST", token, body: datos }),
  registrarSalida: (token, datos) =>
    request("/stock-dosis/salidas", { method: "POST", token, body: datos }),
  stockBajo: (token) => request("/stock-dosis/stock-bajo", { token }),
  vencidos: (token) => request("/stock-dosis/vencidos", { token }),
  puntosSinStock: (token) => request("/stock-dosis/puntos-sin-stock", { token }),
  vacunasEnPunto: (token, puntoId) => request(`/stock-dosis/puntos/${puntoId}/vacunas`, { token }),
};

export const movimientoApi = {
  listar: (token) => request("/movimientos-stock/", { token }),
  ajustar: (token, datos) => request("/movimientos-stock/", { method: "POST", token, body: datos }),
  obtener: (token, id) => request(`/movimientos-stock/${id}`, { token }),
  eliminar: (token, id) => request(`/movimientos-stock/${id}`, { method: "DELETE", token }),
};

export const temperaturaApi = {
  listar: (token, puntoId) =>
    request(`/stock-dosis/temperaturas${puntoId ? `?punto_id=${puntoId}` : ""}`, { token }),
  obtener: (token, id) => request(`/stock-dosis/temperaturas/${id}`, { token }),
  fueraDeRango: (token) => request("/stock-dosis/temperaturas/fuera-de-rango", { token }),
  puntosPendientes: (token) => request("/stock-dosis/temperaturas/puntos-pendientes", { token }),
  registrar: (token, puntoId, datos) =>
    request(`/stock-dosis/temperaturas?punto_id=${puntoId}`, { method: "POST", token, body: datos }),
  eliminar: (token, id) => request(`/stock-dosis/temperaturas/${id}`, { method: "DELETE", token }),
};

export const pacienteApi = {
  listar: (token) => request("/pacientes/", { token }),
  crear: (token, datos) => request("/pacientes/", { method: "POST", token, body: datos }),
  obtener: (token, id) => request(`/pacientes/${id}`, { token }),
  eliminar: (token, id) => request(`/pacientes/${id}`, { method: "DELETE", token }),
  historial: (token, id) => request(`/pacientes/${id}/historial`, { token }),
  agregarAntecedente: (token, id, datos) =>
    request(`/pacientes/${id}/antecedentes`, { method: "POST", token, body: datos }),
};

export const vacunacionApi = {
  registrarDosis: (token, datos) =>
    request("/vacunacion/dosis-aplicadas", { method: "POST", token, body: datos }),
  eliminarRegistro: (token, id) => request(`/vacunacion/registros/${id}`, { method: "DELETE", token }),
  registros: (token) => request("/vacunacion/registros", { token }),
  obtenerRegistro: (token, id) => request(`/vacunacion/registros/${id}`, { token }),
  dosisPendientesPaciente: (token, pacienteId, vacunaId) =>
    request(`/vacunacion/pacientes/${pacienteId}/dosis-pendientes?vacuna_id=${vacunaId}`, { token }),
  refuerzoPendientePaciente: (token, pacienteId, vacunaId) =>
    request(`/vacunacion/pacientes/${pacienteId}/refuerzo-pendiente?vacuna_id=${vacunaId}`, { token }),
  refuerzosPendientes: (token, vacunaId) =>
    request(`/vacunacion/refuerzos-pendientes/pacientes?vacuna_id=${vacunaId}`, { token }),
  dosisPendientes: (token, vacunaId) =>
    request(`/vacunacion/dosis-pendientes/pacientes?vacuna_id=${vacunaId}`, { token }),
};

export const antecedenteApi = {
  listar: (token, pacienteId) =>
    request(`/antecedentes-vacunacion/${pacienteId ? `?paciente_id=${pacienteId}` : ""}`, { token }),
  crear: (token, datos) => request("/antecedentes-vacunacion/", { method: "POST", token, body: datos }),
  obtener: (token, id) => request(`/antecedentes-vacunacion/${id}`, { token }),
  eliminar: (token, id) => request(`/antecedentes-vacunacion/${id}`, { method: "DELETE", token }),
};

export const esquemaApi = {
  listar: (token) => request("/esquemas-vacunacion/", { token }),
  obtener: (token, id) => request(`/esquemas-vacunacion/${id}`, { token }),
  crear: (token, datos) => request("/esquemas-vacunacion/", { method: "POST", token, body: datos }),
  actualizar: (token, id, datos) => request(`/esquemas-vacunacion/${id}`, { method: "PUT", token, body: datos }),
  eliminar: (token, id) => request(`/esquemas-vacunacion/${id}`, { method: "DELETE", token }),
};

export const reporteApi = {
  cobertura: (token, campanaId) => request(`/reportes/cobertura/${campanaId}`, { token }),
};
