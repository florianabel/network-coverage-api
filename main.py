from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()


class ProviderCoverage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    two_g: bool = Field(alias="2G")
    three_g: bool = Field(alias="3G")
    four_g: bool = Field(alias="4G")


class NetworkCoverage(BaseModel):
    orange: Optional[ProviderCoverage]
    sfr: Optional[ProviderCoverage]
    free: Optional[ProviderCoverage]
    bouygue: Optional[ProviderCoverage]


@app.get("/", response_model_by_alias=True)
async def root() -> NetworkCoverage:
    orange = ProviderCoverage(two_g=True, three_g=False, four_g=True,)
    sfr = ProviderCoverage(two_g=True, three_g=False, four_g=True,)
    free = ProviderCoverage(two_g=True, three_g=False, four_g=True,)
    bouyge = ProviderCoverage(two_g=True, three_g=False, four_g=True,)
    coverage = NetworkCoverage(
        orange=orange,
        sfr=sfr,
        free=free,
        bouygue=bouyge,
    )
    return coverage


client = TestClient(app)

def test_root():
    response = client.get("/")
    print(type(response.json()))
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "orange": {"2G": True, "3G": False, "4G": True},
        "sfr": {"2G": True, "3G": False, "4G": True},
        "free": {"2G": True, "3G": False, "4G": True},
        "bouygue": {"2G": True, "3G": False, "4G": True},
    }