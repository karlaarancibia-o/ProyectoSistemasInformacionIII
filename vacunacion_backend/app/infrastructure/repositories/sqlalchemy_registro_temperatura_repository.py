from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.registro_temperatura import RegistroTemperatura
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)
from app.infrastructure.database.models.registro_temperatura import (
    RegistroTemperaturaModel,
)
from app.infrastructure.database.models.vacuna import VacunaModel


def a_entidad(modelo: RegistroTemperaturaModel, db: Session) -> RegistroTemperatura:
    # el rango permitido es el de la VACUNA almacenada, no un rango fijo
    vacuna = db.get(VacunaModel, modelo.vacuna_id)
    return RegistroTemperatura(
        id=modelo.id,
        punto_id=modelo.punto_id,
        vacuna_id=modelo.vacuna_id,
        usuario_id=modelo.usuario_id,
        temperatura_celsius=modelo.temperatura_celsius,
        fecha_hora=modelo.fecha_hora,
        observacion=modelo.observacion,
        rango_minimo=vacuna.temperatura_minima if vacuna else None,
        rango_maximo=vacuna.temperatura_maxima if vacuna else None,
    )


class SqlAlchemyRegistroTemperaturaRepository(RegistroTemperaturaRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[RegistroTemperatura]:
        return [a_entidad(m, self.db) for m in self.db.query(RegistroTemperaturaModel).all()]

    def listar_por_punto(self, punto_id: int) -> list[RegistroTemperatura]:
        modelos = (
            self.db.query(RegistroTemperaturaModel)
            .filter(RegistroTemperaturaModel.punto_id == punto_id)
            .all()
        )
        return [a_entidad(m, self.db) for m in modelos]

    def obtener_por_id(self, registro_id: int) -> RegistroTemperatura | None:
        modelo = self.db.get(RegistroTemperaturaModel, registro_id)
        return a_entidad(modelo, self.db) if modelo else None

    def crear(self, registro: RegistroTemperatura) -> RegistroTemperatura:
        modelo = RegistroTemperaturaModel(
            punto_id=registro.punto_id,
            vacuna_id=registro.vacuna_id,
            usuario_id=registro.usuario_id,
            temperatura_celsius=registro.temperatura_celsius,
            fecha_hora=registro.fecha_hora,
            observacion=registro.observacion,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo, self.db)

    def eliminar(self, registro_id: int) -> None:
        modelo = self.db.get(RegistroTemperaturaModel, registro_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def listar_fuera_de_rango(self) -> list[RegistroTemperatura]:
        modelos = (
            self.db.query(RegistroTemperaturaModel)
            .join(VacunaModel, VacunaModel.id == RegistroTemperaturaModel.vacuna_id)
            .filter(
                (
                    RegistroTemperaturaModel.temperatura_celsius
                    < VacunaModel.temperatura_minima
                )
                | (
                    RegistroTemperaturaModel.temperatura_celsius
                    > VacunaModel.temperatura_maxima
                )
            )
            .all()
        )
        return [a_entidad(m, self.db) for m in modelos]

    def puntos_sin_registro_en_fecha(
        self, puntos_ids: list[int], fecha: date
    ) -> list[int]:
        if not puntos_ids:
            return []
        con_registro = {
            fila[0]
            for fila in self.db.query(RegistroTemperaturaModel.punto_id)
            .filter(
                RegistroTemperaturaModel.punto_id.in_(puntos_ids),
                func.date(RegistroTemperaturaModel.fecha_hora) == fecha,
            )
            .distinct()
            .all()
        }
        return [pid for pid in puntos_ids if pid not in con_registro]
