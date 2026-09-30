from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Contrato para hashear contraseñas.

    La capa application solo conoce este contrato; la implementación real
    (bcrypt/passlib) vive en infrastructure/security.
    """

    @abstractmethod
    def hashear(self, password: str) -> str: ...

    @abstractmethod
    def verificar(self, password_plano: str, password_hash: str) -> bool: ...
