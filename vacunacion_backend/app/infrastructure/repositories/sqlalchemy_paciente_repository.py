from sqlalchemy.orm import Session

from app.domain.entities.paciente import Paciente
from app.domain.repositories.paciente_repository import PacienteRepository
from app.infrastructure.database.models.paciente import PacienteModel


def a_entidad(modelo: PacienteModel) -> Paciente:
    return Paciente(
        id=modelo.id,
        nombres=modelo.nombres,
        apellidos=modelo.apellidos,
        carnet_identidad=modelo.carnet_identidad,
        fecha_nacimiento=modelo.fecha_nacimiento,
        sexo=modelo.sexo,
        telefono=modelo.telefono,
        direccion=modelo.direccion,
        grupo_edad_id=modelo.grupo_edad_id,
    )


class SqlAlchemyPacienteRepository(PacienteRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Paciente]:
        return [a_entidad(m) for m in self.db.query(PacienteModel).all()]

    def obtener_por_id(self, paciente_id: int) -> Paciente | None:
        modelo = self.db.get(PacienteModel, paciente_id)
        return a_entidad(modelo) if modelo else None

    def obtener_por_carnet(self, carnet_identidad: str) -> Paciente | None:
        modelo = (
            self.db.query(PacienteModel)
            .filter(PacienteModel.carnet_identidad == carnet_identidad)
            .first()
        )
        return a_entidad(modelo) if modelo else None

    def crear(self, paciente: Paciente) -> Paciente:
        modelo = PacienteModel(
            nombres=paciente.nombres,
            apellidos=paciente.apellidos,
            carnet_identidad=paciente.carnet_identidad,
            fecha_nacimiento=paciente.fecha_nacimiento,
            sexo=paciente.sexo,
            telefono=paciente.telefono,
            direccion=paciente.direccion,
            grupo_edad_id=paciente.grupo_edad_id,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, paciente_id: int) -> None:
        modelo = self.db.get(PacienteModel, paciente_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
