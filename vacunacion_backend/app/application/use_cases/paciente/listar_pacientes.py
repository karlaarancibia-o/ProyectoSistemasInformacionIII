from app.domain.entities.paciente import Paciente
from app.domain.repositories.paciente_repository import PacienteRepository


class ListarPacientes:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def ejecutar(self) -> list[Paciente]:
        return self.repo.listar()
