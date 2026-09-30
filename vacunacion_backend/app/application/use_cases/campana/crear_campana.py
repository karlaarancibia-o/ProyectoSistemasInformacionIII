from datetime import date

from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository


class CrearCampana:
    """Evento 1: El administrador registra una nueva campaña de vacunación
    estacional."""

    def __init__(
        self,
        repo: CampanaRepository,
        grupo_edad_repo: GrupoEdadRepository,
        vacuna_repo: VacunaRepository,
    ):
        self.repo = repo
        self.grupo_edad_repo = grupo_edad_repo
        self.vacuna_repo = vacuna_repo

    def ejecutar(
        self,
        nombre: str,
        tipo_temporada: str,
        fecha_inicio: date,
        fecha_fin: date,
        vacuna_id: int,
        descripcion: str | None = None,
        grupo_edad_ids: list[int] | None = None,
    ) -> Campana:
        grupo_edad_ids = grupo_edad_ids or []

        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError(f"Vacuna {vacuna_id} no encontrada")
        if not vacuna.esta_activa:
            raise OperacionNoPermitidaError("La vacuna está inactiva")

        # los grupos de edad prioritarios deben existir antes de asociarlos
        for grupo_id in grupo_edad_ids:
            if not self.grupo_edad_repo.obtener_por_id(grupo_id):
                raise NoEncontradoError(f"Grupo de edad {grupo_id} no encontrado")

        # la campaña solo puede dirigirse a grupos para los que la vacuna está indicada
        if vacuna.grupo_edad_ids:
            no_indicados = [g for g in grupo_edad_ids if not vacuna.indicada_para(g)]
            if no_indicados:
                raise OperacionNoPermitidaError(
                    f"La vacuna '{vacuna.nombre}' no está indicada para los grupos de edad "
                    f"{no_indicados}. Grupos indicados: {vacuna.grupo_edad_ids}"
                )
            if not grupo_edad_ids:  # sin grupos explícitos, se usan los de la vacuna
                grupo_edad_ids = list(vacuna.grupo_edad_ids)

        campana = Campana(
            nombre=nombre,
            tipo_temporada=tipo_temporada,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            vacuna_id=vacuna_id,
            descripcion=descripcion,
            grupo_edad_ids=grupo_edad_ids,
        )
        return self.repo.crear(campana)
