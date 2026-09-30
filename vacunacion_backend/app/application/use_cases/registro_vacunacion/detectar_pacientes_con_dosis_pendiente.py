from dataclasses import dataclass
from datetime import date

from app.application.services.esquema_paciente import ServicioEsquemaPaciente
from app.domain.esquema_vacunacion import EsquemaVacunacion
from app.domain.repositories.paciente_repository import PacienteRepository


@dataclass
class PacienteConEsquemaPendiente:
    paciente_id: int
    esquema: EsquemaVacunacion


class DetectarPacientesConDosisPendiente:
    """Evento 25: El sistema detecta que un paciente tiene una dosis
    pendiente. Solo se consideran pacientes cuyo grupo de edad tiene un
    esquema definido para la vacuna."""

    def __init__(
        self, paciente_repo: PacienteRepository, servicio: ServicioEsquemaPaciente
    ):
        self.paciente_repo = paciente_repo
        self.servicio = servicio

    def ejecutar(self, vacuna_id: int) -> list[PacienteConEsquemaPendiente]:
        hoy = date.today()
        pendientes = []
        for paciente in self.paciente_repo.listar():
            esquema = self.servicio.calcular_estado(paciente, vacuna_id, hoy)
            if esquema is not None and esquema.dosis_pendientes > 0:
                pendientes.append(
                    PacienteConEsquemaPendiente(paciente_id=paciente.id, esquema=esquema)
                )
        return pendientes
