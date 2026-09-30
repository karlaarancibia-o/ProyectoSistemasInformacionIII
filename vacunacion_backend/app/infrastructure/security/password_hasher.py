from passlib.context import CryptContext

from app.application.interfaces.password_hasher import PasswordHasher

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher(PasswordHasher):
    def hashear(self, password: str) -> str:
        return _pwd_context.hash(password)

    def verificar(self, password_plano: str, password_hash: str) -> bool:
        return _pwd_context.verify(password_plano, password_hash)
