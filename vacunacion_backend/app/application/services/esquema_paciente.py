"""Servicio de aplicación: junta los datos (paciente, grupos de edad,
esquemas, dosis aplicadas y antecedentes) que hacen falta para decidir qué
dosis le corresponde a un paciente. Lo usan el registro de dosis y todas las
consultas de dosis/refuerzos pendientes."""

import unicodedata
from datetime import date

from app.domain.entities.esquema_vacunacion import EsquemaVacunacion as ReglaEsquema
from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.entities.paciente import Paciente
from app.domain.esquema_vacunacion import DosisPrevia, EsquemaVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.reglas_edad import calcular_edad, grupos_para_edad
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)
from app.domain.repositories.vacuna_repository import VacunaRepository


def _normalizar(texto: str) -> str:
    sin_tildes = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return " ".join(sin_tildes.lower().split())


class ServicioEsquemaPaciente:
    def __init__(
        self,
        registro_repo: RegistroVacunacionRepository,
        antecedente_repo: AntecedenteVacunacionRepository,
        esquema_repo: EsquemaVacunacionRepository,
        grupo_repo: GrupoEdadRepository,
        vacuna_repo: VacunaRepository,
    ):
        self.registro_repo = registro_repo
        self.antecedente_repo = antecedente_repo
        self.esquema_repo = esquema_repo
        self.grupo_repo = grupo_repo
        self.vacuna_repo = vacuna_repo

    def grupos_para_edad(self, edad: int) -> list[GrupoEdad]:
        return grupos_para_edad(self.grupo_repo.listar(), edad)

    def grupos_indicados(
        self, vacuna_id: int, grupos: list[GrupoEdad]
    ) -> tuple[str, list[GrupoEdad]]:
        """Nombre de la vacuna y, de `grupos`, solo aquellos para los que está indicada."""
        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError("Vacuna no encontrada")
        return vacuna.nombre, [g for g in grupos if vacuna.indicada_para(g.id)]

    def regla_para(
        self, vacuna_id: int, grupos: list[GrupoEdad]
    ) -> ReglaEsquema | None:
        """Esquema de la vacuna para el primer grupo (por prioridad) que lo tenga."""
        esquemas = [e for e in self.esquema_repo.listar() if e.vacuna_id == vacuna_id]
        for grupo in grupos:
            for esquema in esquemas:
                if esquema.grupo_edad_id == grupo.id:
                    return esquema
        return None

    def dosis_previas(self, paciente_id: int, vacuna_id: int) -> list[DosisPrevia]:
        """Dosis de esa vacuna ya aplicadas al paciente: las registradas en el
        sistema y los antecedentes (dosis previas fuera del sistema) cuyo
        nombre de vacuna coincide con el de la vacuna del catálogo."""
        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError("Vacuna no encontrada")

        previas = [
            DosisPrevia(fecha=r.fecha_aplicacion, es_refuerzo=r.es_refuerzo)
            for r in self.registro_repo.listar_por_paciente(paciente_id)
            if r.vacuna_id == vacuna_id
        ]
        nombre = _normalizar(vacuna.nombre)
        previas += [
            DosisPrevia(fecha=a.fecha_aplicacion, es_refuerzo=False)
            for a in self.antecedente_repo.listar_por_paciente(paciente_id)
            if _normalizar(a.vacuna) == nombre
        ]
        return previas

    def calcular_estado(
        self, paciente: Paciente, vacuna_id: int, hoy: date
    ) -> EsquemaVacunacion | None:
        """Estado del paciente para la vacuna. None si no existe un esquema
        definido para la vacuna y el grupo de edad del paciente."""
        edad = calcular_edad(paciente.fecha_nacimiento, hoy)
        regla = self.regla_para(vacuna_id, self.grupos_para_edad(edad))
        if regla is None:
            return None
        return EsquemaVacunacion.calcular(
            paciente_id=paciente.id,
            vacuna_id=vacuna_id,
            regla=regla,
            previas=self.dosis_previas(paciente.id, vacuna_id),
            hoy=hoy,
        )
