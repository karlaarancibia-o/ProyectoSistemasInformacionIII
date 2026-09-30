from datetime import date

from app.application.services.esquema_paciente import ServicioEsquemaPaciente
from app.domain.esquema_vacunacion import EsquemaVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.paciente_repository import PacienteRepository


class ConsultarDosisPendientes:
    """Evento 21: El administrador consulta las dosis pendientes de un
    paciente para una vacuna (según el esquema de su grupo de edad)."""

    def __init__(
        self, paciente_repo: PacienteRepository, servicio: ServicioEsquemaPaciente
    ):
        self.paciente_repo = paciente_repo
        self.servicio = servicio

    def ejecutar(self, paciente_id: int, vacuna_id: int) -> EsquemaVacunacion:
        paciente = self.paciente_repo.obtener_por_id(paciente_id)
        if not paciente:
            raise NoEncontradoError("Paciente no encontrado")

        esquema = self.servicio.calcular_estado(paciente, vacuna_id, date.today())
        if esquema is None:
            raise NoEncontradoError(
                "No hay un esquema de vacunación definido para esta vacuna y "
                "el grupo de edad del paciente"
            )
        return esquema
