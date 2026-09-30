from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.exceptions import OperacionNoPermitidaError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository


class AsignarGrupoEdadACampana:
    """El administrador asigna un grupo de edad prioritario a una campaña ya
    existente."""

    def __init__(
        self,
        campana_repo: CampanaRepository,
        grupo_edad_repo: GrupoEdadRepository,
        vacuna_repo: VacunaRepository,
    ):
        self.campana_repo = campana_repo
        self.grupo_edad_repo = grupo_edad_repo
        self.vacuna_repo = vacuna_repo

    def ejecutar(self, campana_id: int, grupo_edad_id: int) -> Campana:
        campana = self.campana_repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")
        if not self.grupo_edad_repo.obtener_por_id(grupo_edad_id):
            raise NoEncontradoError("Grupo de edad no encontrado")

        vacuna = self.vacuna_repo.obtener_por_id(campana.vacuna_id)
        if vacuna and not vacuna.indicada_para(grupo_edad_id):
            raise OperacionNoPermitidaError(
                f"La vacuna '{vacuna.nombre}' de la campaña no está indicada para ese grupo de edad"
            )

        campana.asignar_grupo_edad(grupo_edad_id)  # valida duplicados
        return self.campana_repo.actualizar(campana)
