from app.application.use_cases.esquema_vacunacion.obtener_esquema_vacunacion import (
    ObtenerEsquemaVacunacion,
)
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)


class EliminarEsquemaVacunacion:
    def __init__(self, repo: EsquemaVacunacionRepository):
        self.repo = repo

    def ejecutar(self, esquema_id: int) -> None:
        ObtenerEsquemaVacunacion(self.repo).ejecutar(esquema_id)
        self.repo.eliminar(esquema_id)
