from datetime import date

from sqlalchemy.orm import Session

from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.infrastructure.database.models.lote_dosis import LoteDosisModel


def a_entidad(modelo: LoteDosisModel) -> LoteDosis:
    return LoteDosis(
        id=modelo.id,
        vacuna_id=modelo.vacuna_id,
        numero_lote=modelo.numero_lote,
        fecha_fabricacion=modelo.fecha_fabricacion,
        fecha_vencimiento=modelo.fecha_vencimiento,
        cantidad_inicial=modelo.cantidad_inicial,
        cantidad_actual=modelo.cantidad_actual,
        umbral_minimo=modelo.umbral_minimo,
        punto_id=modelo.punto_id,
    )


class SqlAlchemyLoteDosisRepository(LoteDosisRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[LoteDosis]:
        return [a_entidad(m) for m in self.db.query(LoteDosisModel).all()]

    def listar_por_punto(self, punto_id: int | None) -> list[LoteDosis]:
        filtro = (
            LoteDosisModel.punto_id.is_(None)
            if punto_id is None
            else LoteDosisModel.punto_id == punto_id
        )
        modelos = self.db.query(LoteDosisModel).filter(filtro).all()
        return [a_entidad(m) for m in modelos]

    def obtener_por_id(self, lote_id: int) -> LoteDosis | None:
        modelo = self.db.get(LoteDosisModel, lote_id)
        return a_entidad(modelo) if modelo else None

    def buscar_lote(
        self, vacuna_id: int, numero_lote: str, punto_id: int | None
    ) -> LoteDosis | None:
        filtro_punto = (
            LoteDosisModel.punto_id.is_(None)
            if punto_id is None
            else LoteDosisModel.punto_id == punto_id
        )
        modelo = (
            self.db.query(LoteDosisModel)
            .filter(
                LoteDosisModel.vacuna_id == vacuna_id,
                LoteDosisModel.numero_lote == numero_lote,
                filtro_punto,
            )
            .first()
        )
        return a_entidad(modelo) if modelo else None

    def crear(self, lote: LoteDosis) -> LoteDosis:
        modelo = LoteDosisModel(
            vacuna_id=lote.vacuna_id,
            numero_lote=lote.numero_lote,
            fecha_fabricacion=lote.fecha_fabricacion,
            fecha_vencimiento=lote.fecha_vencimiento,
            cantidad_inicial=lote.cantidad_inicial,
            cantidad_actual=lote.cantidad_actual,
            umbral_minimo=lote.umbral_minimo,
            punto_id=lote.punto_id,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def actualizar(self, lote: LoteDosis) -> LoteDosis:
        modelo = self.db.get(LoteDosisModel, lote.id)
        modelo.cantidad_inicial = lote.cantidad_inicial
        modelo.cantidad_actual = lote.cantidad_actual
        modelo.umbral_minimo = lote.umbral_minimo
        modelo.fecha_vencimiento = lote.fecha_vencimiento
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, lote_id: int) -> None:
        modelo = self.db.get(LoteDosisModel, lote_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()

    def listar_con_stock_bajo(self) -> list[LoteDosis]:
        modelos = (
            self.db.query(LoteDosisModel)
            .filter(LoteDosisModel.cantidad_actual <= LoteDosisModel.umbral_minimo)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def listar_vencidos(self, hoy: date) -> list[LoteDosis]:
        modelos = (
            self.db.query(LoteDosisModel)
            .filter(LoteDosisModel.fecha_vencimiento < hoy)
            .all()
        )
        return [a_entidad(m) for m in modelos]
