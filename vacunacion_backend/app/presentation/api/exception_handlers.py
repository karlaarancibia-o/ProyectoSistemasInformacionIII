from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.domain.exceptions import (
    CredencialesInvalidasError,
    DatosInvalidosError,
    DominioError,
    NoAutenticadoError,
    NoEncontradoError,
    OperacionNoPermitidaError,
    PermisoDenegadoError,
    YaExisteError,
)

_CODIGOS_HTTP = {
    NoEncontradoError: 404,
    YaExisteError: 400,
    CredencialesInvalidasError: 401,
    NoAutenticadoError: 401,
    PermisoDenegadoError: 403,
    DatosInvalidosError: 422,
    OperacionNoPermitidaError: 409,
}


def registrar_manejadores_de_errores(app: FastAPI):
    @app.exception_handler(DominioError)
    async def manejar_error_de_dominio(request: Request, exc: DominioError):
        codigo = next(
            (c for tipo, c in _CODIGOS_HTTP.items() if isinstance(exc, tipo)),
            400,
        )
        return JSONResponse(status_code=codigo, content={"detail": str(exc)})

    @app.exception_handler(IntegrityError)
    async def manejar_error_de_integridad(request: Request, exc: IntegrityError):
        # p. ej. borrar algo que otros registros todavía referencian, o un
        # dato único duplicado que no se validó antes
        return JSONResponse(
            status_code=409,
            content={
                "detail": "La operación viola una restricción de integridad: el "
                "registro está siendo usado por otros datos o ya existe."
            },
        )
