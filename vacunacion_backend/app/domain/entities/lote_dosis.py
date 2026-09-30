from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import DatosInvalidosError


@dataclass
class LoteDosis:
    vacuna_id: int
    numero_lote: str
    fecha_fabricacion: date
    fecha_vencimiento: date
    cantidad_inicial: int
    umbral_minimo: int
    id: int | None = None
    cantidad_actual: int | None = None
    punto_id: int | None = None  # None = almacén central

    def __post_init__(self):
        if self.cantidad_actual is None:
            self.cantidad_actual = self.cantidad_inicial
        if not self.numero_lote.strip():
            raise DatosInvalidosError("El número de lote es obligatorio")
        if self.fecha_vencimiento <= self.fecha_fabricacion:
            raise DatosInvalidosError(
                "La fecha de vencimiento debe ser posterior a la de fabricación"
            )
        if self.cantidad_inicial < 0:
            raise DatosInvalidosError("La cantidad inicial no puede ser negativa")
        if self.cantidad_actual < 0:
            raise DatosInvalidosError("La cantidad actual no puede ser negativa")
        if self.umbral_minimo < 0:
            raise DatosInvalidosError("El umbral mínimo no puede ser negativo")

    def esta_vencido(self, hoy: date) -> bool:
        return self.fecha_vencimiento < hoy

    def vence_dentro_de(self, hoy: date, dias: int) -> bool:
        return hoy <= self.fecha_vencimiento <= hoy.fromordinal(hoy.toordinal() + dias)

    @property
    def stock_bajo(self) -> bool:
        return self.cantidad_actual <= self.umbral_minimo

    def descontar(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad a descontar debe ser positiva")
        if cantidad > self.cantidad_actual:
            raise DatosInvalidosError("No hay suficiente stock disponible en el lote")
        self.cantidad_actual -= cantidad

    def incrementar(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad a incrementar debe ser positiva")
        self.cantidad_actual += cantidad
