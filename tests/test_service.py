from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    body = response.json()
    assert "version" in body
    assert isinstance(body["version"], str)
    assert len(body["version"]) > 0
