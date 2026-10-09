from typing import Dict, List, Optional

from core.doc_const import DOCUMENTS
from core.logger import logger
from models.schemas import DocumentCreate, DocumentSearch


def get_all_documents(
    doc_type: Optional[str] = None,
    year: Optional[int] = None,
) -> List[Dict]:
    logger.debug("get_all_documents: doc_type=%r, year=%r", doc_type, year)

    result: List[Dict] = list(DOCUMENTS.values())

    if doc_type is not None:
        result = [doc for doc in result if doc["type"] == doc_type]

    if year is not None:
        result = [doc for doc in result if doc["year"] == year]

    logger.info("get_all_documents: returned %d documents", len(result))
    return result


def get_document_by_id(document_id: int) -> Optional[Dict]:
    logger.debug("get_document_by_id: document_id=%r", document_id)

    document = DOCUMENTS.get(document_id)

    if document is None:
        logger.warning("get_document_by_id: document %s not found", document_id)
    else:
        logger.info("get_document_by_id: found '%s'", document["title"])

    return document


def find_document_by_full_match(query: DocumentSearch) -> Optional[Dict]:
    logger.debug(
        "find_document_by_full_match: title=%r, author=%r, year=%r, type=%r",
        query.title, query.author, query.year, query.type,
    )

    for document in DOCUMENTS.values():
        if (
            document["title"] == query.title
            and document["author"] == query.author
            and document["year"] == query.year
            and document["type"] == query.type
        ):
            logger.info("find_document_by_full_match: found id=%s", document["id"])
            return document

    logger.warning("find_document_by_full_match: no match for %r", query.title)
    return None


def create_document(payload: DocumentCreate) -> Dict:
    logger.debug(
        "create_document: title=%r, author=%r, year=%r, type=%r",
        payload.title, payload.author, payload.year, payload.type,
    )

    new_id = max(DOCUMENTS.keys(), default=0) + 1

    document = {
        "id": new_id,
        "title": payload.title,
        "author": payload.author,
        "year": payload.year,
        "type": payload.type,
    }

    DOCUMENTS[new_id] = document
    logger.info("create_document: created id=%s, title=%r", new_id, payload.title)

    return document