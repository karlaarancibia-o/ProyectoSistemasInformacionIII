import os

from fastapi import FastAPI

from app.infrastructure.database import models  # noqa: F401
from app.application.use_cases.auth.asegurar_administrador_inicial import AsegurarAdministradorInicial
from app.infrastructure.database.connection import Base, SessionLocal, engine
from app.infrastructure.database.migraciones import permitir_almacen_central
from app.infrastructure.repositories.sqlalchemy_usuario_repository import SqlAlchemyUsuarioRepository
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.presentation.api.exception_handlers import registrar_manejadores_de_errores
from app.presentation.api.middlewares import configurar_middlewares
from app.presentation.api.routers import (
    antecedentes_vacunacion,
    auth,
    campanas,
    esquemas_vacunacion,
    grupos_edad,
    movimientos_stock,
    pacientes,
    puntos_vacunacion,
    reportes,
    stock_dosis,
    vacunas,
    vacunacion,
)

Base.metadata.create_all(bind=engine)
permitir_almacen_central(engine)  # el almacén central usa punto_id = NULL

# Si no hay ningún administrador activo y se definió ADMIN_USERNAME / ADMIN_PASSWORD
# en el .env, se crea (o promueve) esa cuenta como administrador.
with SessionLocal() as _db:
    AsegurarAdministradorInicial(
        SqlAlchemyUsuarioRepository(_db), BcryptPasswordHasher()
    ).ejecutar(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))

app = FastAPI(title="Sistema de Gestión de Campañas de Vacunación por Temporada")

configurar_middlewares(app)
registrar_manejadores_de_errores(app)

app.include_router(auth.router)
app.include_router(campanas.router)
app.include_router(grupos_edad.router)
app.include_router(puntos_vacunacion.router)
app.include_router(pacientes.router)
app.include_router(antecedentes_vacunacion.router)
app.include_router(vacunas.router)
app.include_router(esquemas_vacunacion.router)
app.include_router(stock_dosis.router)
app.include_router(movimientos_stock.router)
app.include_router(vacunacion.router)
app.include_router(reportes.router)
