# ZipVacunación — Frontend (React + Vite)

Frontend del Sistema de Gestión de Campañas de Vacunación. Misma estructura que el proyecto de ejemplo
(`api/client.js`, `context/AuthContext.jsx`, `pages/`), más `components/` para el layout.

## Ejecutar
```bash
cp .env.example .env      # VITE_API_URL apunta al backend (por defecto http://127.0.0.1:8000)
npm install
npm run dev               # http://localhost:5173
```
El backend debe estar corriendo (`uvicorn app.presentation.main:app --reload`).

## Estructura
- `src/api/client.js` — todas las llamadas HTTP (auth, grupos de edad, vacunas, campañas, pacientes, registros)
- `src/context/AuthContext.jsx` — sesión (token en localStorage) y datos del usuario (`/auth/me`)
- `src/components/` — `Layout` (header + sidebar), `Calendario`, `Icons`
- `src/pages/` — `Login`, `Inicio`, `GruposEdad`, `Vacunas`, `Campanas`, `Pacientes`, `RegistrarDosis`, `Registros`, `Puntos`, `Stock`, `CadenaFrio`, `Perfil`

## Avance
| Módulo | Estado |
|---|---|
| Login / registro / sesión | Listo |
| Inicio (dashboard con datos reales) | Listo |
| Grupos de edad (CRUD) | Listo |
| Vacunas (CRUD, selección de grupos de edad) | Listo |
| Campañas (crear, activar/finalizar, asignar puntos) | Listo |
| Pacientes (registro, historial, antecedentes) | Listo |
| Registrar dosis (campaña → punto → lote) | Listo |
| Registros de vacunación | Listo |
| Puntos de vacunación (CRUD + horarios de atención) | Listo |
| Stock de dosis (entradas, salidas, lotes, ajustes, alertas) | Listo |
| Cadena de frío (temperaturas, fuera de rango, pendientes) | Listo |
| Perfil y administración de usuarios (roles, activar/desactivar) | Listo |

El menú lateral se ajusta al rol: personal de salud ve pacientes/dosis/registros, logística ve stock y cadena de frío, y el administrador ve todo.
