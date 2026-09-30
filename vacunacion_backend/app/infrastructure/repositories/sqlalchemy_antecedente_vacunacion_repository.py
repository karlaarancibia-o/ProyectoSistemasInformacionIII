from sqlalchemy.orm import Session

from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)
from app.infrastructure.database.models.antecedente_vacunacion import (
    AntecedenteVacunacionModel,
)


def a_entidad(modelo: AntecedenteVacunacionModel) -> AntecedenteVacunacion:
    return AntecedenteVacunacion(
        id=modelo.id,
        paciente_id=modelo.paciente_id,
        vacuna=modelo.vacuna,
        fecha_aplicacion=modelo.fecha_aplicacion,
        numero_dosis=modelo.numero_dosis,
        observaciones=modelo.observaciones,
    )


class SqlAlchemyAntecedenteVacunacionRepository(AntecedenteVacunacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[AntecedenteVacunacion]:
        return [a_entidad(m) for m in self.db.query(AntecedenteVacunacionModel).all()]

    def listar_por_paciente(self, paciente_id: int) -> list[AntecedenteVacunacion]:
        modelos = (
            self.db.query(AntecedenteVacunacionModel)
            .filter(AntecedenteVacunacionModel.paciente_id == paciente_id)
            .all()
        )
        return [a_entidad(m) for m in modelos]

    def obtener_por_id(self, antecedente_id: int) -> AntecedenteVacunacion | None:
        modelo = self.db.get(AntecedenteVacunacionModel, antecedente_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, antecedente: AntecedenteVacunacion) -> AntecedenteVacunacion:
        modelo = AntecedenteVacunacionModel(
            paciente_id=antecedente.paciente_id,
            vacuna=antecedente.vacuna,
            fecha_aplicacion=antecedente.fecha_aplicacion,
            numero_dosis=antecedente.numero_dosis,
            observaciones=antecedente.observaciones,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, antecedente_id: int) -> None:
        modelo = self.db.get(AntecedenteVacunacionModel, antecedente_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
