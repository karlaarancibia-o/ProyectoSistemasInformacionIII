from datetime import date

from app.domain.entities.paciente import Paciente
from app.domain.exceptions import (
    DatosInvalidosError,
    NoEncontradoError,
    YaExisteError,
)
from app.domain.reglas_edad import calcular_edad, grupos_para_edad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository


class RegistrarPaciente:
    """Evento 6: El personal de salud registra un nuevo paciente.

    El grupo de edad debe ser coherente con la fecha de nacimiento: si se
    indica uno, la edad del paciente tiene que estar dentro de su rango; si
    no se indica, se asigna automáticamente el que le corresponde.
    """

    def __init__(
        self, repo: PacienteRepository, grupo_edad_repo: GrupoEdadRepository
    ):
        self.repo = repo
        self.grupo_edad_repo = grupo_edad_repo

    def ejecutar(
        self,
        nombres: str,
        apellidos: str,
        carnet_identidad: str,
        fecha_nacimiento: date,
        sexo: str,
        telefono: str | None = None,
        direccion: str | None = None,
        grupo_edad_id: int | None = None,
    ) -> Paciente:
        carnet_identidad = carnet_identidad.strip()
        paciente = Paciente(  # valida datos básicos
            nombres=nombres,
            apellidos=apellidos,
            carnet_identidad=carnet_identidad,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            telefono=telefono,
            direccion=direccion,
            grupo_edad_id=grupo_edad_id,
        )
        if self.repo.obtener_por_carnet(carnet_identidad):
            raise YaExisteError("Ya existe un paciente con ese carnet de identidad")

        edad = calcular_edad(fecha_nacimiento, date.today())
        if grupo_edad_id is not None:
            grupo = self.grupo_edad_repo.obtener_por_id(grupo_edad_id)
            if not grupo:
                raise NoEncontradoError("Grupo de edad no encontrado")
            if not grupo.contiene_edad(edad):
                raise DatosInvalidosError(
                    f"El paciente tiene {edad} años y no corresponde al grupo de edad "
                    f"'{grupo.nombre}' ({grupo.edad_min}–{grupo.edad_max} años)"
                )
        else:
            candidatos = grupos_para_edad(self.grupo_edad_repo.listar(), edad)
            paciente.grupo_edad_id = candidatos[0].id if candidatos else None

        return self.repo.crear(paciente)
