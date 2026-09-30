"""Errores del dominio.

No dependen de FastAPI ni de HTTP: la capa de presentacion los traduce
a codigos de estado (404, 400, 409...).
"""


class DominioError(Exception):
    """Clase base de todos los errores de negocio."""


class NoEncontradoError(DominioError):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class YaExisteError(DominioError):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class DatosInvalidosError(DominioError):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class OperacionNoPermitidaError(DominioError):
    """La operación es válida en sí, pero el estado actual no la permite
    (ej. registrar dosis de una campaña finalizada, activar una campaña dos veces).
    """

    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class CredencialesInvalidasError(DominioError):
    def __init__(self):
        super().__init__("Credenciales inválidas.")


class PermisoDenegadoError(DominioError):
    """El usuario está autenticado pero su rol no permite la acción."""

    def __init__(self, mensaje: str = "No tiene permisos para esta acción"):
        super().__init__(mensaje)


class NoAutenticadoError(DominioError):
    """Token inválido/expirado o usuario del token inexistente."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
