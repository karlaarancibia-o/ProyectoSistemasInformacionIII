from datetime import date

from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.reglas_edad import calcular_edad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository


class ActualizarGrupoEdad:
    """El administrador edita un grupo de edad completo (nombre, rango de
    edades, prioridad y descripción).

    No se permite un rango que se superponga con otro grupo, ni uno que deje
    fuera a pacientes ya asignados a este grupo.
    """

    def __init__(self, repo: GrupoEdadRepository, paciente_repo: PacienteRepository):
        self.repo = repo
        self.paciente_repo = paciente_repo

    def ejecutar(
        self,
        grupo_id: int,
        nombre: str,
        edad_min: int,
        edad_max: int,
        prioridad: int,
        descripcion: str | None = None,
    ) -> GrupoEdad:
        if not self.repo.obtener_por_id(grupo_id):
            raise NoEncontradoError("Grupo de edad no encontrado")

        grupo = GrupoEdad(
            id=grupo_id,
            nombre=nombre,
            edad_min=edad_min,
            edad_max=edad_max,
            prioridad=prioridad,
            descripcion=descripcion,
        )

        for otro in self.repo.listar():
            if otro.id != grupo_id and grupo.se_superpone_con(otro):
                raise OperacionNoPermitidaError(
                    f"El rango {edad_min}–{edad_max} se superpone con el grupo '{otro.nombre}' "
                    f"({otro.edad_min}–{otro.edad_max})"
                )

        hoy = date.today()
        for paciente in self.paciente_repo.listar():
            if paciente.grupo_edad_id == grupo_id and not grupo.contiene_edad(
                calcular_edad(paciente.fecha_nacimiento, hoy)
            ):
                raise OperacionNoPermitidaError(
                    "El nuevo rango dejaría fuera a pacientes ya asignados a este grupo "
                    f"(por ejemplo {paciente.nombres} {paciente.apellidos})"
                )
        return self.repo.actualizar(grupo)
