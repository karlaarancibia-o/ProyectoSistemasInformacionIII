from app.application.use_cases.registro_temperatura.obtener_registro_temperatura import (
    ObtenerRegistroTemperatura,
)
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)


class EliminarRegistroTemperatura:
    def __init__(self, repo: RegistroTemperaturaRepository):
        self.repo = repo

    def ejecutar(self, registro_id: int) -> None:
        ObtenerRegistroTemperatura(self.repo).ejecutar(registro_id)
        self.repo.eliminar(registro_id)
