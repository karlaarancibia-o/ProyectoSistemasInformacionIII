from app.application.use_cases.punto_vacunacion.obtener_punto_vacunacion import (
    ObtenerPuntoVacunacion,
)
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class EliminarPuntoVacunacion:
    def __init__(self, repo: PuntoVacunacionRepository):
        self.repo = repo

    def ejecutar(self, punto_id: int) -> None:
        ObtenerPuntoVacunacion(self.repo).ejecutar(punto_id)
        self.repo.eliminar(punto_id)
