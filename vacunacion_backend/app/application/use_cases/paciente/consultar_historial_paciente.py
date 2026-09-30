from dataclasses import dataclass

from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion
from app.domain.entities.registro_vacunacion import RegistroVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)


@dataclass
class HistorialPaciente:
    antecedentes: list[AntecedenteVacunacion]
    dosis_aplicadas_en_el_sistema: list[RegistroVacunacion]


class ConsultarHistorialPaciente:
    """Evento 20: El personal de salud consulta el historial de vacunación
    de un paciente."""

    def __init__(
        self,
        paciente_repo: PacienteRepository,
        antecedente_repo: AntecedenteVacunacionRepository,
        registro_repo: RegistroVacunacionRepository,
    ):
        self.paciente_repo = paciente_repo
        self.antecedente_repo = antecedente_repo
        self.registro_repo = registro_repo

    def ejecutar(self, paciente_id: int) -> HistorialPaciente:
        if not self.paciente_repo.obtener_por_id(paciente_id):
            raise NoEncontradoError("Paciente no encontrado")

        return HistorialPaciente(
            antecedentes=self.antecedente_repo.listar_por_paciente(paciente_id),
            dosis_aplicadas_en_el_sistema=self.registro_repo.listar_por_paciente(
                paciente_id
            ),
        )
