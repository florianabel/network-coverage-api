from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_network_coverage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "orange": {"2G": True, "3G": False, "4G": True},
        "sfr": {"2G": True, "3G": False, "4G": True},
        "free": {"2G": True, "3G": False, "4G": True},
        "bouygue": {"2G": True, "3G": False, "4G": True},
    }