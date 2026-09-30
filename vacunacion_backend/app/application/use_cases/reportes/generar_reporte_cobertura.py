from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import NoEncontradoError
from app.domain.reglas_edad import calcular_edad
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)


@dataclass
class ReporteCobertura:
    campana_id: int
    nombre_campana: str
    total_pacientes_registrados: int
    total_dosis_aplicadas: int
    pacientes_vacunados: int
    porcentaje_cobertura: float
    total_pacientes_objetivo: int = 0


class GenerarReporteCobertura:
    """Evento 28: El administrador consulta el reporte de cobertura de
    vacunación.

    La cobertura se mide sobre la población OBJETIVO de la campaña (pacientes
    cuya edad actual está en alguno de sus grupos de edad; si la campaña no
    define grupos, todos los pacientes)."""

    def __init__(
        self,
        campana_repo: CampanaRepository,
        paciente_repo: PacienteRepository,
        registro_repo: RegistroVacunacionRepository,
        grupo_repo: GrupoEdadRepository,
    ):
        self.campana_repo = campana_repo
        self.paciente_repo = paciente_repo
        self.registro_repo = registro_repo
        self.grupo_repo = grupo_repo

    def ejecutar(self, campana_id: int) -> ReporteCobertura:
        campana = self.campana_repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")

        registros = self.registro_repo.listar_por_campana(campana_id)
        pacientes_vacunados = {r.paciente_id for r in registros}
        pacientes = self.paciente_repo.listar()

        if campana.grupo_edad_ids:
            hoy = date.today()
            grupos = [
                g for g in self.grupo_repo.listar() if g.id in campana.grupo_edad_ids
            ]
            objetivo = [
                p
                for p in pacientes
                if any(
                    g.contiene_edad(calcular_edad(p.fecha_nacimiento, hoy))
                    for g in grupos
                )
            ]
        else:
            objetivo = pacientes
        ids_objetivo = {p.id for p in objetivo}
        vacunados_objetivo = len(pacientes_vacunados & ids_objetivo)

        porcentaje = (
            (vacunados_objetivo / len(ids_objetivo)) * 100 if ids_objetivo else 0.0
        )

        return ReporteCobertura(
            campana_id=campana_id,
            nombre_campana=campana.nombre,
            total_pacientes_registrados=len(pacientes),
            total_dosis_aplicadas=len(registros),
            pacientes_vacunados=len(pacientes_vacunados),
            porcentaje_cobertura=round(porcentaje, 2),
            total_pacientes_objetivo=len(ids_objetivo),
        )
