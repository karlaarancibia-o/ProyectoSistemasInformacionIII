from abc import ABC, abstractmethod


class TokenService(ABC):
    """Contrato para crear y leer tokens de sesión.

    La implementación real (JWT) vive en infrastructure/security.
    """

    @abstractmethod
    def crear(self, data: dict) -> str: ...

    @abstractmethod
    def decodificar(self, token: str) -> dict | None:
        """Devuelve el contenido del token o None si es inválido/expirado."""
