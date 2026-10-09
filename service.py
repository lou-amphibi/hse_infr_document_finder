from typing import Dict, List, Optional

from doc_const import DOCUMENTS


def get_all_documents(
    doc_type: Optional[str] = None,
    year: Optional[int] = None,
) -> List[Dict]:
    result: List[Dict] = list(DOCUMENTS.values())

    if doc_type is not None:
        result = [doc for doc in result if doc["type"] == doc_type]

    if year is not None:
        result = [doc for doc in result if doc["year"] == year]

    return result


def get_document_by_id(document_id: int) -> Optional[Dict]:
    return DOCUMENTS.get(document_id)

