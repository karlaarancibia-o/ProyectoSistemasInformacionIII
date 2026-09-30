from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)


class ObtenerAntecedenteVacunacion:
    def __init__(self, repo: AntecedenteVacunacionRepository):
        self.repo = repo

    def ejecutar(self, antecedente_id: int) -> AntecedenteVacunacion:
        antecedente = self.repo.obtener_por_id(antecedente_id)
        if not antecedente:
            raise NoEncontradoError("Antecedente de vacunación no encontrado")
        return antecedente
