from app.domain.entities.registro_vacunacion import RegistroVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)


class ObtenerRegistroVacunacion:
    def __init__(self, repo: RegistroVacunacionRepository):
        self.repo = repo

    def ejecutar(self, registro_id: int) -> RegistroVacunacion:
        registro = self.repo.obtener_por_id(registro_id)
        if not registro:
            raise NoEncontradoError("Registro de vacunación no encontrado")
        return registro
