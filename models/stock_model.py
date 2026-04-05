from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field


class Gusto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    peso_balde: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    activo: bool = True


class Ingreso(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha: date
    gusto_id: int = Field(foreign_key="gusto.id")
    cantidad: float  # 👈 SIEMPRE en kilos
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Conteo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha: date
    gusto_id: int = Field(foreign_key="gusto.id")
    cantidad: float  # 👈 también en kilos
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))