from typing import Dict, List, Optional
from logger import logger
from doc_const import DOCUMENTS


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

