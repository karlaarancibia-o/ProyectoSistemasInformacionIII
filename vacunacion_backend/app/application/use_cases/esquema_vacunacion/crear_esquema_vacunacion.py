from app.domain.entities.esquema_vacunacion import EsquemaVacunacion
from app.domain.exceptions import (
    NoEncontradoError,
    OperacionNoPermitidaError,
    YaExisteError,
)
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository


class CrearEsquemaVacunacion:
    """El administrador define la regla de vacunación de una vacuna para un
    grupo de edad:

    - cantidad_dosis: dosis de la serie primaria.
    - dias_entre_dosis: intervalo mínimo entre dosis de esa serie (0 si es
      una sola dosis).
    - requiere_refuerzo / meses_refuerzo: dosis adicional que se aplica cada
      X meses después de completar la serie.

    Hay un solo esquema por combinación vacuna + grupo de edad.
    """

    def __init__(
        self,
        repo: EsquemaVacunacionRepository,
        vacuna_repo: VacunaRepository,
        grupo_edad_repo: GrupoEdadRepository,
    ):
        self.repo = repo
        self.vacuna_repo = vacuna_repo
        self.grupo_edad_repo = grupo_edad_repo

    def ejecutar(
        self,
        vacuna_id: int,
        grupo_edad_id: int,
        cantidad_dosis: int,
        dias_entre_dosis: int,
        requiere_refuerzo: bool = False,
        meses_refuerzo: int | None = None,
    ) -> EsquemaVacunacion:
        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError("Vacuna no encontrada")
        if not vacuna.esta_activa:
            raise OperacionNoPermitidaError("La vacuna está inactiva")
        if not self.grupo_edad_repo.obtener_por_id(grupo_edad_id):
            raise NoEncontradoError("Grupo de edad no encontrado")
        if not vacuna.indicada_para(grupo_edad_id):
            raise OperacionNoPermitidaError(
                f"La vacuna '{vacuna.nombre}' no está indicada para ese grupo de edad"
            )

        if not requiere_refuerzo and meses_refuerzo == 0:
            meses_refuerzo = None  # sin refuerzo, 0 equivale a "vacío"; un valor > 0 sí se rechaza

        esquema = EsquemaVacunacion(
            vacuna_id=vacuna_id,
            grupo_edad_id=grupo_edad_id,
            cantidad_dosis=cantidad_dosis,
            dias_entre_dosis=dias_entre_dosis,
            requiere_refuerzo=requiere_refuerzo,
            meses_refuerzo=meses_refuerzo,
        )
        esquema.validar_coherencia()

        if any(
            e.vacuna_id == vacuna_id and e.grupo_edad_id == grupo_edad_id
            for e in self.repo.listar()
        ):
            raise YaExisteError(
                "Ya existe un esquema para esta vacuna y este grupo de edad"
            )
        return self.repo.crear(esquema)
