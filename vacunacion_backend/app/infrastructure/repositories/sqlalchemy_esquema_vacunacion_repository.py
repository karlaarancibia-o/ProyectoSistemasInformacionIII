from sqlalchemy.orm import Session

from app.domain.entities.esquema_vacunacion import EsquemaVacunacion
from app.domain.repositories.esquema_vacunacion_repository import (
    EsquemaVacunacionRepository,
)
from app.infrastructure.database.models.esquema_vacunacion import (
    EsquemaVacunacionModel,
)


def a_entidad(modelo: EsquemaVacunacionModel) -> EsquemaVacunacion:
    return EsquemaVacunacion(
        id=modelo.id,
        vacuna_id=modelo.vacuna_id,
        grupo_edad_id=modelo.grupo_edad_id,
        cantidad_dosis=modelo.cantidad_dosis,
        dias_entre_dosis=modelo.dias_entre_dosis,
        requiere_refuerzo=modelo.requiere_refuerzo,
        meses_refuerzo=modelo.meses_refuerzo,
    )


class SqlAlchemyEsquemaVacunacionRepository(EsquemaVacunacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[EsquemaVacunacion]:
        return [a_entidad(m) for m in self.db.query(EsquemaVacunacionModel).all()]

    def obtener_por_id(self, esquema_id: int) -> EsquemaVacunacion | None:
        modelo = self.db.get(EsquemaVacunacionModel, esquema_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, esquema: EsquemaVacunacion) -> EsquemaVacunacion:
        modelo = EsquemaVacunacionModel(
            vacuna_id=esquema.vacuna_id,
            grupo_edad_id=esquema.grupo_edad_id,
            cantidad_dosis=esquema.cantidad_dosis,
            dias_entre_dosis=esquema.dias_entre_dosis,
            requiere_refuerzo=esquema.requiere_refuerzo,
            meses_refuerzo=esquema.meses_refuerzo,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def actualizar(self, esquema: EsquemaVacunacion) -> EsquemaVacunacion:
        modelo = self.db.get(EsquemaVacunacionModel, esquema.id)
        modelo.vacuna_id = esquema.vacuna_id
        modelo.grupo_edad_id = esquema.grupo_edad_id
        modelo.cantidad_dosis = esquema.cantidad_dosis
        modelo.dias_entre_dosis = esquema.dias_entre_dosis
        modelo.requiere_refuerzo = esquema.requiere_refuerzo
        modelo.meses_refuerzo = esquema.meses_refuerzo
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, esquema_id: int) -> None:
        modelo = self.db.get(EsquemaVacunacionModel, esquema_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
