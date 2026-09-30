from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class ActualizarPuntoVacunacion:
    """Complementa el evento 3 (diagrama nivel 2: 'Actualizar punto'): el
    administrador corrige los datos de un punto de vacunación ya
    registrado. No modifica las campañas asociadas: eso se gestiona con
    AsignarPuntoACampana / QuitarPuntoDeCampana."""

    def __init__(self, repo: PuntoVacunacionRepository):
        self.repo = repo

    def ejecutar(
        self,
        punto_id: int,
        nombre: str,
        direccion: str,
        capacidad: int,
        telefono: str | None = None,
        estado: str = "activo",
    ) -> PuntoVacunacion:
        punto = self.repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")

        punto.nombre = nombre
        punto.direccion = direccion
        punto.capacidad = capacidad
        punto.telefono = telefono
        punto.estado = estado
        PuntoVacunacion(**vars(punto))  # revalida invariantes del dominio

        return self.repo.actualizar(punto)
