from app.application.use_cases.paciente.obtener_paciente import ObtenerPaciente
from app.domain.repositories.paciente_repository import PacienteRepository


class EliminarPaciente:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def ejecutar(self, paciente_id: int) -> None:
        ObtenerPaciente(self.repo).ejecutar(paciente_id)
        self.repo.eliminar(paciente_id)
