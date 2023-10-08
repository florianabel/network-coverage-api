from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_network_coverage():
    response = client.get("/?q=42+rue+papernest+75011+Paris")
    assert response.status_code == 200
    assert response.json() == {
        "orange": {
            "2G": True,
            "3G": True,
            "4G": False,
        },
        "sfr": {
            "2G": True,
            "3G": False,
            "4G": False,
        },
        "free": {
            "2G": False,
            "3G": True,
            "4G": True,
        },
        "bouygue": {
            "2G": True,
            "3G": False,
            "4G": False,
        },
    }