from app.application.use_cases.antecedente_vacunacion.obtener_antecedente_vacunacion import (
    ObtenerAntecedenteVacunacion,
)
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)


class EliminarAntecedenteVacunacion:
    def __init__(self, repo: AntecedenteVacunacionRepository):
        self.repo = repo

    def ejecutar(self, antecedente_id: int) -> None:
        ObtenerAntecedenteVacunacion(self.repo).ejecutar(antecedente_id)
        self.repo.eliminar(antecedente_id)
