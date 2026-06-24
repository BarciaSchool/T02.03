from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Tecnología"])
    descripcion: str | None = Field(
        default=None, max_length=255, examples=["Productos electrónicos y gadgets"]
    )


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaOut(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
