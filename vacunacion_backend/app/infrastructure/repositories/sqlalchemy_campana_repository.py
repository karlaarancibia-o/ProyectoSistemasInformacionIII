from datetime import date

from sqlalchemy.orm import Session

from app.domain.entities.campana import Campana
from app.domain.repositories.campana_repository import CampanaRepository
from app.infrastructure.database.models.campana import CampanaModel
from app.infrastructure.database.models.grupo_edad import GrupoEdadModel
from app.infrastructure.database.models.punto_vacunacion import PuntoVacunacionModel


def a_entidad(modelo: CampanaModel) -> Campana:
    return Campana(
        id=modelo.id,
        nombre=modelo.nombre,
        descripcion=modelo.descripcion,
        tipo_temporada=modelo.tipo_temporada,
        fecha_inicio=modelo.fecha_inicio,
        fecha_fin=modelo.fecha_fin,
        vacuna_id=modelo.vacuna_id,
        estado=modelo.estado,
        grupo_edad_ids=[g.id for g in modelo.grupos_edad],
        punto_ids=[p.id for p in modelo.puntos],
    )


class SqlAlchemyCampanaRepository(CampanaRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Campana]:
        return [a_entidad(m) for m in self.db.query(CampanaModel).all()]

    def listar_activas(self) -> list[Campana]:
        modelos = self.db.query(CampanaModel).filter(CampanaModel.estado == "activa").all()
        return [a_entidad(m) for m in modelos]

    def listar_planificadas_desde(self, fecha_inicio: date) -> list[Campana]:
        modelos = (
            self.db.query(CampanaModel)
            .filter(
                CampanaModel.estado == "planificada",
                CampanaModel.fecha_inicio <= fecha_inicio,
            )
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def listar_activas_hasta(self, fecha_fin: date) -> list[Campana]:
        modelos = (
            self.db.query(CampanaModel)
            .filter(CampanaModel.estado == "activa", CampanaModel.fecha_fin <= fecha_fin)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def obtener_por_id(self, campana_id: int) -> Campana | None:
        modelo = self.db.get(CampanaModel, campana_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, campana: Campana) -> Campana:
        modelo = CampanaModel(
            nombre=campana.nombre,
            descripcion=campana.descripcion,
            tipo_temporada=campana.tipo_temporada,
            fecha_inicio=campana.fecha_inicio,
            fecha_fin=campana.fecha_fin,
            vacuna_id=campana.vacuna_id,
            estado=campana.estado,
        )
        if campana.grupo_edad_ids:
            modelo.grupos_edad = (
                self.db.query(GrupoEdadModel)
                .filter(GrupoEdadModel.id.in_(campana.grupo_edad_ids))
                .all()
            )
        if campana.punto_ids:
            modelo.puntos = (
                self.db.query(PuntoVacunacionModel)
                .filter(PuntoVacunacionModel.id.in_(campana.punto_ids))
                .all()
            )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, campana_id: int) -> None:
        modelo = self.db.get(CampanaModel, campana_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def actualizar(self, campana: Campana) -> Campana:
        modelo = self.db.get(CampanaModel, campana.id)
        modelo.nombre = campana.nombre
        modelo.descripcion = campana.descripcion
        modelo.tipo_temporada = campana.tipo_temporada
        modelo.fecha_inicio = campana.fecha_inicio
        modelo.fecha_fin = campana.fecha_fin
        modelo.vacuna_id = campana.vacuna_id
        modelo.estado = campana.estado
        modelo.grupos_edad = (
            self.db.query(GrupoEdadModel)
            .filter(GrupoEdadModel.id.in_(campana.grupo_edad_ids))
            .all()
            if campana.grupo_edad_ids
            else []
        )
        modelo.puntos = (
            self.db.query(PuntoVacunacionModel)
            .filter(PuntoVacunacionModel.id.in_(campana.punto_ids))
            .all()
            if campana.punto_ids
            else []
        )
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)
