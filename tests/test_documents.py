from fastapi.testclient import TestClient

from core.doc_const import DOCUMENTS


def test_list_documents(client: TestClient) -> None:
    response = client.get("/documents")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == len(DOCUMENTS)


def test_get_document_by_id(client: TestClient) -> None:
    response = client.get("/documents/7")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 7
    assert body["title"] == "Устав НИУ ВШЭ"


def test_get_document_not_found(client: TestClient) -> None:
    response = client.get("/documents/99999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_search_document_found(client: TestClient) -> None:
    payload = {
        "title": "Устав НИУ ВШЭ",
        "author": "Учёный совет",
        "year": 2019,
        "type": "нормативный",
    }
    response = client.post("/documents/search", json=payload)

    assert response.status_code == 200
    assert response.json()["id"] == 7


def test_search_document_not_found(client: TestClient) -> None:
    payload = {
        "title": "Несуществующий документ",
        "author": "Никто",
        "year": 2020,
        "type": "x",
    }
    response = client.post("/documents/search", json=payload)

    assert response.status_code == 404


def test_create_document(client: TestClient) -> None:
    payload = {
        "title": "Тестовый документ",
        "author": "Иван Иванов",
        "year": 2026,
        "type": "учебный",
    }
    response = client.post("/documents", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["author"] == payload["author"]
    assert "id" in body
    assert body["id"] in DOCUMENTS


def test_create_document_invalid(client: TestClient) -> None:
    payload = {
        "title": "",
        "author": "A",
        "year": 1800,
        "type": "x",
    }
    response = client.post("/documents", json=payload)

    assert response.status_code == 422


def test_delete_document(client: TestClient) -> None:
    response = client.delete("/documents/7")

    assert response.status_code == 204
    assert response.content == b""
    assert 7 not in DOCUMENTS


def test_delete_document_not_found(client: TestClient) -> None:
    response = client.delete("/documents/99999")

    assert response.status_code == 404
