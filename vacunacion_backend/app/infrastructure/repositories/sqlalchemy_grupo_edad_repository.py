from sqlalchemy.orm import Session

from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.infrastructure.database.models.grupo_edad import GrupoEdadModel


def a_entidad(modelo: GrupoEdadModel) -> GrupoEdad:
    return GrupoEdad(
        id=modelo.id,
        nombre=modelo.nombre,
        edad_min=modelo.edad_min,
        edad_max=modelo.edad_max,
        prioridad=modelo.prioridad,
        descripcion=modelo.descripcion,
    )


class SqlAlchemyGrupoEdadRepository(GrupoEdadRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[GrupoEdad]:
        return [a_entidad(m) for m in self.db.query(GrupoEdadModel).all()]

    def obtener_por_id(self, grupo_id: int) -> GrupoEdad | None:
        modelo = self.db.get(GrupoEdadModel, grupo_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, grupo: GrupoEdad) -> GrupoEdad:
        modelo = GrupoEdadModel(
            nombre=grupo.nombre,
            edad_min=grupo.edad_min,
            edad_max=grupo.edad_max,
            prioridad=grupo.prioridad,
            descripcion=grupo.descripcion,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, grupo_id: int) -> None:
        modelo = self.db.get(GrupoEdadModel, grupo_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def actualizar(self, grupo: GrupoEdad) -> GrupoEdad:
        modelo = self.db.get(GrupoEdadModel, grupo.id)
        modelo.nombre = grupo.nombre
        modelo.edad_min = grupo.edad_min
        modelo.edad_max = grupo.edad_max
        modelo.prioridad = grupo.prioridad
        modelo.descripcion = grupo.descripcion
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)
