from app.domain.entities.paciente import Paciente
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.paciente_repository import PacienteRepository


class ObtenerPaciente:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def ejecutar(self, paciente_id: int) -> Paciente:
        paciente = self.repo.obtener_por_id(paciente_id)
        if not paciente:
            raise NoEncontradoError("Paciente no encontrado")
        return paciente
