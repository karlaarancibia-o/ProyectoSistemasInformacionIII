from sqlalchemy.orm import Session

from app.domain.entities.horario_atencion import HorarioAtencion
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)
from app.infrastructure.database.models.horario_atencion import HorarioAtencionModel


def a_entidad(modelo: HorarioAtencionModel) -> HorarioAtencion:
    return HorarioAtencion(
        id=modelo.id,
        punto_id=modelo.punto_id,
        dia_semana=modelo.dia_semana,
        hora_apertura=modelo.hora_apertura,
        hora_cierre=modelo.hora_cierre,
    )


class SqlAlchemyHorarioAtencionRepository(HorarioAtencionRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[HorarioAtencion]:
        return [a_entidad(m) for m in self.db.query(HorarioAtencionModel).all()]

    def listar_por_punto(self, punto_id: int) -> list[HorarioAtencion]:
        modelos = (
            self.db.query(HorarioAtencionModel)
            .filter(HorarioAtencionModel.punto_id == punto_id)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def obtener_por_id(self, horario_id: int) -> HorarioAtencion | None:
        modelo = self.db.get(HorarioAtencionModel, horario_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, horario: HorarioAtencion) -> HorarioAtencion:
        modelo = HorarioAtencionModel(
            punto_id=horario.punto_id,
            dia_semana=horario.dia_semana,
            hora_apertura=horario.hora_apertura,
            hora_cierre=horario.hora_cierre,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, horario_id: int) -> None:
        modelo = self.db.get(HorarioAtencionModel, horario_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def actualizar(self, horario: HorarioAtencion) -> HorarioAtencion:
        modelo = self.db.get(HorarioAtencionModel, horario.id)
        modelo.dia_semana = horario.dia_semana
        modelo.hora_apertura = horario.hora_apertura
        modelo.hora_cierre = horario.hora_cierre
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)
