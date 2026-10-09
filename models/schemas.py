from pydantic import BaseModel, Field


class DocumentSearch(BaseModel):
    """Тело запроса для поиска документа по полному совпадению."""
    title: str = Field(..., min_length=1, description="Название документа")
    author: str = Field(..., min_length=1, description="Автор документа")
    year: int = Field(..., ge=1900, le=2100, description="Год издания")
    type: str = Field(..., min_length=1, description="Тип документа")


class DocumentCreate(BaseModel):
    """Тело запроса для создания нового документа."""
    title: str = Field(..., min_length=1, description="Название документа")
    author: str = Field(..., min_length=1, description="Автор документа")
    year: int = Field(..., ge=1900, le=2100, description="Год издания")
    type: str = Field(..., min_length=1, description="Тип документа")




