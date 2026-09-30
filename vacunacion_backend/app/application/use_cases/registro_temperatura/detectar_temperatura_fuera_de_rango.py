from app.domain.entities.registro_temperatura import RegistroTemperatura
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)


class DetectarTemperaturaFueraDeRango:
    """Evento 24: La temperatura de almacenamiento sale del rango permitido."""

    def __init__(self, repo: RegistroTemperaturaRepository):
        self.repo = repo

    def ejecutar(self) -> list[RegistroTemperatura]:
        return self.repo.listar_fuera_de_rango()
