from app.domain.entities.esquema_vacunacion import EsquemaVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)


class ObtenerEsquemaVacunacion:
    def __init__(self, repo: EsquemaVacunacionRepository):
        self.repo = repo

    def ejecutar(self, esquema_id: int) -> EsquemaVacunacion:
        esquema = self.repo.obtener_por_id(esquema_id)
        if not esquema:
            raise NoEncontradoError("Esquema de vacunación no encontrado")
        return esquema
