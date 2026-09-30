from app.domain.entities.registro_temperatura import RegistroTemperatura
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)


class ObtenerRegistroTemperatura:
    def __init__(self, repo: RegistroTemperaturaRepository):
        self.repo = repo

    def ejecutar(self, registro_id: int) -> RegistroTemperatura:
        registro = self.repo.obtener_por_id(registro_id)
        if not registro:
            raise NoEncontradoError("Registro de temperatura no encontrado")
        return registro
