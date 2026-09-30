"""Importar todos los modelos aquí para que se registren en Base.metadata
(lo usa app.infrastructure.database.connection.Base.metadata.create_all)."""

from app.infrastructure.database.models.antecedente_vacunacion import (  # noqa: F401
    AntecedenteVacunacionModel,
)
from app.infrastructure.database.models.campana import CampanaModel  # noqa: F401
from app.infrastructure.database.models.esquema_vacunacion import (  # noqa: F401
    EsquemaVacunacionModel,
)
from app.infrastructure.database.models.grupo_edad import GrupoEdadModel  # noqa: F401
from app.infrastructure.database.models.horario_atencion import (  # noqa: F401
    HorarioAtencionModel,
)
from app.infrastructure.database.models.lote_dosis import LoteDosisModel  # noqa: F401
from app.infrastructure.database.models.movimiento_stock import (  # noqa: F401
    MovimientoStockModel,
)
from app.infrastructure.database.models.paciente import PacienteModel  # noqa: F401
from app.infrastructure.database.models.punto_vacunacion import (  # noqa: F401
    PuntoVacunacionModel,
)
from app.infrastructure.database.models.registro_temperatura import (  # noqa: F401
    RegistroTemperaturaModel,
)
from app.infrastructure.database.models.registro_vacunacion import (  # noqa: F401
    RegistroVacunacionModel,
)
from app.infrastructure.database.models.usuario import UsuarioModel  # noqa: F401
from app.infrastructure.database.models.vacuna import VacunaModel  # noqa: F401
