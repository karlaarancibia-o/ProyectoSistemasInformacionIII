from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)


class ListarAntecedentesVacunacion:
    def __init__(self, repo: AntecedenteVacunacionRepository):
        self.repo = repo

    def ejecutar(self, paciente_id: int | None = None) -> list[AntecedenteVacunacion]:
        if paciente_id is not None:
            return self.repo.listar_por_paciente(paciente_id)
        return self.repo.listar()
