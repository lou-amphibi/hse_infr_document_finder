from typing import Optional

from fastapi import FastAPI, HTTPException

from service import get_all_documents, get_document_by_id

app = FastAPI(title="HSE Document Finder")


@app.get("/documents")
def list_documents(
    doc_type: Optional[str] = None,
    year: Optional[int] = None,
):
    return get_all_documents(doc_type=doc_type, year=year)


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    document = get_document_by_id(document_id)
    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Документ с id={document_id} не найден",
        )
    return document


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.2v"}

