from typing import Generator

import pytest
from fastapi.testclient import TestClient

from core.doc_const import DOCUMENTS
from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    backup = DOCUMENTS.copy()

    with TestClient(app) as test_client:
        yield test_client

    DOCUMENTS.clear()
    DOCUMENTS.update(backup)
