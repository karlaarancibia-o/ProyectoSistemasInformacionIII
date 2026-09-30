from app.domain.entities.registro_vacunacion import RegistroVacunacion
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)


class ListarRegistrosVacunacion:
    def __init__(self, repo: RegistroVacunacionRepository):
        self.repo = repo

    def ejecutar(self) -> list[RegistroVacunacion]:
        return self.repo.listar_todos()
