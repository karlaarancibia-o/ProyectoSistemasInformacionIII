from sqlalchemy.orm import Session

from app.domain.entities.vacuna import Vacuna
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.infrastructure.database.models.grupo_edad import GrupoEdadModel
from app.infrastructure.database.models.vacuna import VacunaModel


def a_entidad(modelo: VacunaModel) -> Vacuna:
    return Vacuna(
        id=modelo.id,
        nombre=modelo.nombre,
        fabricante=modelo.fabricante,
        tipo=modelo.tipo,
        descripcion=modelo.descripcion,
        temperatura_minima=modelo.temperatura_minima,
        temperatura_maxima=modelo.temperatura_maxima,
        estado=modelo.estado,
        grupo_edad_ids=sorted(g.id for g in modelo.grupos_edad),
    )


class SqlAlchemyVacunaRepository(VacunaRepository):
    def __init__(self, db: Session):
        self.db = db

    def _grupos(self, ids: list[int]) -> list[GrupoEdadModel]:
        if not ids:
            return []
        return self.db.query(GrupoEdadModel).filter(GrupoEdadModel.id.in_(ids)).all()

    def listar(self) -> list[Vacuna]:
        return [a_entidad(m) for m in self.db.query(VacunaModel).all()]

    def obtener_por_id(self, vacuna_id: int) -> Vacuna | None:
        modelo = self.db.get(VacunaModel, vacuna_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, vacuna: Vacuna) -> Vacuna:
        modelo = VacunaModel(
            nombre=vacuna.nombre,
            fabricante=vacuna.fabricante,
            tipo=vacuna.tipo,
            descripcion=vacuna.descripcion,
            temperatura_minima=vacuna.temperatura_minima,
            temperatura_maxima=vacuna.temperatura_maxima,
            estado=vacuna.estado,
            grupos_edad=self._grupos(vacuna.grupo_edad_ids),
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def actualizar(self, vacuna: Vacuna) -> Vacuna:
        modelo = self.db.get(VacunaModel, vacuna.id)
        modelo.nombre = vacuna.nombre
        modelo.fabricante = vacuna.fabricante
        modelo.tipo = vacuna.tipo
        modelo.descripcion = vacuna.descripcion
        modelo.temperatura_minima = vacuna.temperatura_minima
        modelo.temperatura_maxima = vacuna.temperatura_maxima
        modelo.estado = vacuna.estado
        modelo.grupos_edad = self._grupos(vacuna.grupo_edad_ids)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, vacuna_id: int) -> None:
        modelo = self.db.get(VacunaModel, vacuna_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
