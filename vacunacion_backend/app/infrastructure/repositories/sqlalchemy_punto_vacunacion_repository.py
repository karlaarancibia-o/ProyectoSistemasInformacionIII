from sqlalchemy.orm import Session

from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.infrastructure.database.models.campana import CampanaModel
from app.infrastructure.database.models.punto_vacunacion import PuntoVacunacionModel


def a_entidad(modelo: PuntoVacunacionModel) -> PuntoVacunacion:
    return PuntoVacunacion(
        id=modelo.id,
        nombre=modelo.nombre,
        direccion=modelo.direccion,
        capacidad=modelo.capacidad,
        telefono=modelo.telefono,
        estado=modelo.estado,
        campana_ids=[c.id for c in modelo.campanas],
    )


class SqlAlchemyPuntoVacunacionRepository(PuntoVacunacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[PuntoVacunacion]:
        return [a_entidad(m) for m in self.db.query(PuntoVacunacionModel).all()]

    def obtener_por_id(self, punto_id: int) -> PuntoVacunacion | None:
        modelo = self.db.get(PuntoVacunacionModel, punto_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, punto: PuntoVacunacion) -> PuntoVacunacion:
        modelo = PuntoVacunacionModel(
            nombre=punto.nombre,
            direccion=punto.direccion,
            capacidad=punto.capacidad,
            telefono=punto.telefono,
            estado=punto.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, punto_id: int) -> None:
        modelo = self.db.get(PuntoVacunacionModel, punto_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def actualizar(self, punto: PuntoVacunacion) -> PuntoVacunacion:
        modelo = self.db.get(PuntoVacunacionModel, punto.id)
        modelo.nombre = punto.nombre
        modelo.direccion = punto.direccion
        modelo.capacidad = punto.capacidad
        modelo.telefono = punto.telefono
        modelo.estado = punto.estado
        modelo.campanas = (
            self.db.query(CampanaModel)
            .filter(CampanaModel.id.in_(punto.campana_ids))
            .all()
            if punto.campana_ids
            else []
        )
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)
