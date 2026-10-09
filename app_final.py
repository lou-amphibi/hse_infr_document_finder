from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException

from doc_const import DOCUMENTS
from logger import logger
from service import get_all_documents, get_document_by_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("HSE Document Finder — starting up")
    logger.info("Loaded %d documents into memory", len(DOCUMENTS))
    logger.info("Docs available at http://127.0.0.1:8000/docs")
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info("HSE Document Finder — shutting down")
    logger.info("=" * 60)


app = FastAPI(title="HSE Document Finder", lifespan=lifespan)


@app.get("/documents")
def list_documents(
    doc_type: Optional[str] = None,
    year: Optional[int] = None,
):
    logger.info("GET /documents — doc_type=%r, year=%r", doc_type, year)
    documents = get_all_documents(doc_type=doc_type, year=year)
    logger.info("GET /documents — responding with %d documents", len(documents))
    return documents


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    logger.info("GET /documents/%s — incoming request", document_id)
    document = get_document_by_id(document_id)
    if document is None:
        logger.warning("GET /documents/%s — not found", document_id)
        raise HTTPException(
            status_code=404,
            detail=f"Документ с id={document_id} не найден",
        )
    logger.info("GET /documents/%s — found '%s'", document_id, document["title"])
    return document


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.1v"}
