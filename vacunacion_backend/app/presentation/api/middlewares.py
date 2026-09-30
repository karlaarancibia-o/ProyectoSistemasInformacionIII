import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


def configurar_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        inicio = time.time()
        response = await call_next(request)
        duracion = time.time() - inicio
        print(f"{request.method} {request.url.path} - {response.status_code} - {duracion:.3f}s")
        return response

    @app.middleware("http")
    async def manejar_errores(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            return JSONResponse(status_code=500, content={"detail": f"Error interno: {exc}"})
