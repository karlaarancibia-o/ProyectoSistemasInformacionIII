from pydantic import BaseModel, ConfigDict, Field


class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6)
    rol: str | None = Field(
        default=None,
        description="administrador, personal_salud o logistica. Solo un administrador puede "
        "asignar un rol distinto de personal_salud; si se omite se usa personal_salud.",
    )


class UsuarioResponse(BaseModel):
    id: int
    username: str
    rol: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class CambiarRolRequest(BaseModel):
    rol: str = Field(..., pattern="^(administrador|personal_salud|logistica)$")


class CambiarEstadoRequest(BaseModel):
    activo: bool


class RolResponse(BaseModel):
    rol: str
    descripcion: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
