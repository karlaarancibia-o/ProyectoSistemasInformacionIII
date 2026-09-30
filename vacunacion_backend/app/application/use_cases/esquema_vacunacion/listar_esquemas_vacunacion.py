from app.domain.entities.esquema_vacunacion import EsquemaVacunacion
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)


class ListarEsquemasVacunacion:
    def __init__(self, repo: EsquemaVacunacionRepository):
        self.repo = repo

    def ejecutar(self) -> list[EsquemaVacunacion]:
        return self.repo.listar()
