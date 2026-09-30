from app.application.interfaces.password_hasher import PasswordHasher
from app.domain.entities.usuario import Usuario
from app.domain.exceptions import PermisoDenegadoError, YaExisteError
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.domain.roles import ADMINISTRADOR, PERSONAL_SALUD, validar_rol


class RegistrarUsuario:
    """Alta de usuarios.

    - Si el sistema no tiene ningún administrador activo, la cuenta creada
      pasa a ser administrador (arranque inicial).
    - Un administrador puede crear usuarios con cualquier rol.
    - Cualquier otro solicitante (registro público) solo puede crear cuentas
      de personal de salud, y solo si el registro público está habilitado.
    """

    def __init__(
        self,
        repo: UsuarioRepository,
        hasher: PasswordHasher,
        registro_publico_habilitado: bool = True,
    ):
        self.repo = repo
        self.hasher = hasher
        self.registro_publico_habilitado = registro_publico_habilitado

    def ejecutar(
        self,
        username: str,
        password: str,
        rol: str | None = None,
        solicitante: Usuario | None = None,
    ) -> Usuario:
        username = username.strip()
        rol_pedido = validar_rol(rol)

        if self.repo.contar_administradores_activos() == 0:
            rol_final = ADMINISTRADOR  # primera cuenta / sistema sin administrador
        elif solicitante is not None and solicitante.es_administrador:
            rol_final = rol_pedido
        else:
            if not self.registro_publico_habilitado:
                raise PermisoDenegadoError(
                    "El registro público está deshabilitado: solicite la cuenta a un administrador"
                )
            if rol_pedido != PERSONAL_SALUD:
                raise PermisoDenegadoError(
                    "Solo un administrador puede crear cuentas con ese rol"
                )
            rol_final = PERSONAL_SALUD

        if self.repo.obtener_por_username(username):
            raise YaExisteError("El nombre de usuario ya existe.")

        return self.repo.crear(
            Usuario(
                username=username,
                password_hash=self.hasher.hashear(password),
                rol=rol_final,
            )
        )
