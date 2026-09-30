from app.domain.entities.registro_temperatura import RegistroTemperatura
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)


class ListarRegistrosTemperatura:
    def __init__(self, repo: RegistroTemperaturaRepository):
        self.repo = repo

    def ejecutar(self, punto_id: int | None = None) -> list[RegistroTemperatura]:
        if punto_id is not None:
            return self.repo.listar_por_punto(punto_id)
        return self.repo.listar()
