from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def root():
    return {
        "orange": {"2G": True, "3G": True, "4G": False}, 
        "SFR": {"2G": True, "3G": True, "4G": True}
    }


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "orange": {"2G": True, "3G": True, "4G": False}, 
        "SFR": {"2G": True, "3G": True, "4G": True}
    }