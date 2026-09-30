from sqlalchemy.orm import Session

from app.domain.entities.registro_vacunacion import RegistroVacunacion
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)
from app.infrastructure.database.models.registro_vacunacion import (
    RegistroVacunacionModel,
)


def a_entidad(modelo: RegistroVacunacionModel) -> RegistroVacunacion:
    return RegistroVacunacion(
        id=modelo.id,
        paciente_id=modelo.paciente_id,
        campana_id=modelo.campana_id,
        punto_id=modelo.punto_id,
        lote_id=modelo.lote_id,
        vacuna_id=modelo.vacuna_id,
        fecha_aplicacion=modelo.fecha_aplicacion,
        numero_dosis=modelo.numero_dosis,
        es_refuerzo=modelo.es_refuerzo,
    )


class SqlAlchemyRegistroVacunacionRepository(RegistroVacunacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar_por_paciente(self, paciente_id: int) -> list[RegistroVacunacion]:
        modelos = (
            self.db.query(RegistroVacunacionModel)
            .filter(RegistroVacunacionModel.paciente_id == paciente_id)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def listar_por_campana(self, campana_id: int) -> list[RegistroVacunacion]:
        modelos = (
            self.db.query(RegistroVacunacionModel)
            .filter(RegistroVacunacionModel.campana_id == campana_id)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def crear(self, registro: RegistroVacunacion) -> RegistroVacunacion:
        modelo = RegistroVacunacionModel(
            paciente_id=registro.paciente_id,
            campana_id=registro.campana_id,
            punto_id=registro.punto_id,
            lote_id=registro.lote_id,
            vacuna_id=registro.vacuna_id,
            fecha_aplicacion=registro.fecha_aplicacion,
            numero_dosis=registro.numero_dosis,
            es_refuerzo=registro.es_refuerzo,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def listar_todos(self) -> list[RegistroVacunacion]:
        return [a_entidad(m) for m in self.db.query(RegistroVacunacionModel).all()]

    def obtener_por_id(self, registro_id: int) -> RegistroVacunacion | None:
        modelo = self.db.get(RegistroVacunacionModel, registro_id)
        return a_entidad(modelo) if modelo else None

    def eliminar(self, registro_id: int) -> None:
        modelo = self.db.get(RegistroVacunacionModel, registro_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
