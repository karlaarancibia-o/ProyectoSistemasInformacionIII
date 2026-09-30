from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.campana_repository import CampanaRepository


class QuitarGrupoEdadDeCampana:
    def __init__(self, campana_repo: CampanaRepository):
        self.campana_repo = campana_repo

    def ejecutar(self, campana_id: int, grupo_edad_id: int) -> Campana:
        campana = self.campana_repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")

        campana.quitar_grupo_edad(grupo_edad_id)  # valida que estuviera asignado
        return self.campana_repo.actualizar(campana)
