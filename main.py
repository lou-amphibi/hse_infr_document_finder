from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException

from core.doc_const import DOCUMENTS
from core.logger import logger
from models.schemas import DocumentCreate, DocumentSearch

from service.service import (
    create_document,
    find_document_by_full_match,
    get_all_documents,
    get_document_by_id,
)


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


@app.post("/documents", status_code=201)
def create_new_document(payload: DocumentCreate):
    logger.info(
        "POST /documents — title=%r, author=%r, year=%r, type=%r",
        payload.title, payload.author, payload.year, payload.type,
    )

    document = create_document(payload)

    logger.info("POST /documents — created id=%s, responding with 201", document["id"])
    return document


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


@app.post("/documents/search")
def search_document(query: DocumentSearch):
    logger.info(
        "POST /documents/search — title=%r, author=%r, year=%r, type=%r",
        query.title, query.author, query.year, query.type,
    )

    document = find_document_by_full_match(query)

    if document is None:
        logger.warning("POST /documents/search — no match, returning 404")
        raise HTTPException(
            status_code=404,
            detail="Документ с такими параметрами не найден",
        )

    logger.info("POST /documents/search — found id=%s", document["id"])
    return document


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.3v"}
