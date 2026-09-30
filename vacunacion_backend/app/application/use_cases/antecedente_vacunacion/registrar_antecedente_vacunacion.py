from datetime import date

from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion
from app.domain.exceptions import (
    DatosInvalidosError,
    NoEncontradoError,
    YaExisteError,
)
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)
from app.domain.repositories.paciente_repository import PacienteRepository


class RegistrarAntecedenteVacunacion:
    """Evento 7: El personal de salud registra los antecedentes de
    vacunación (dosis aplicadas previamente, fuera de este sistema).

    Estos antecedentes cuentan para el esquema del paciente cuando el nombre
    de la vacuna coincide con el de una vacuna del catálogo."""

    def __init__(
        self, repo: AntecedenteVacunacionRepository, paciente_repo: PacienteRepository
    ):
        self.repo = repo
        self.paciente_repo = paciente_repo

    def ejecutar(
        self,
        paciente_id: int,
        vacuna: str,
        fecha_aplicacion: date,
        numero_dosis: int,
        observaciones: str | None = None,
    ) -> AntecedenteVacunacion:
        paciente = self.paciente_repo.obtener_por_id(paciente_id)
        if not paciente:
            raise NoEncontradoError("Paciente no encontrado")

        antecedente = AntecedenteVacunacion(
            paciente_id=paciente_id,
            vacuna=vacuna.strip(),
            fecha_aplicacion=fecha_aplicacion,
            numero_dosis=numero_dosis,
            observaciones=observaciones,
        )
        if fecha_aplicacion < paciente.fecha_nacimiento:
            raise DatosInvalidosError(
                "La fecha de aplicación es anterior a la fecha de nacimiento del paciente"
            )
        if any(
            a.vacuna.strip().lower() == antecedente.vacuna.lower()
            and a.numero_dosis == numero_dosis
            for a in self.repo.listar_por_paciente(paciente_id)
        ):
            raise YaExisteError(
                f"El paciente ya tiene registrada la dosis {numero_dosis} de {antecedente.vacuna}"
            )
        return self.repo.crear(antecedente)
