import requests
from typing import Optional, Literal, Union

from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import BaseModel, Field, ConfigDict, conlist

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


class Geometry(BaseModel):
    type: Literal["Point"]
    coordinates: conlist(float, min_length=2, max_length=2)


class Housenumber(BaseModel):
    label: str
    score: float
    housenumber: str
    id: str
    name: str
    postcode: str
    citycode: str
    x: float
    y: float
    city: str
    district: str
    context: str
    type: Literal["housenumber"]
    importance: float
    street: str


class Street(BaseModel):
    label: str
    score: float
    id: str
    name: str
    postcode: str
    citycode: str
    x: float
    y: float
    city: str
    district: str
    context: str
    type: Literal["street"]
    importance: float
    street: str


class Feature(BaseModel):
    feature_type: Literal["Feature"] = Field(alias='type')
    geometry: Geometry
    properties: Union[Street, Housenumber]


@app.get("/", response_model_by_alias=True)
async def root(q: str) -> NetworkCoverage:
    print(q)
    response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={q}")
    res_json = response.json()
    if features := res_json.get('features', None):
        for feature in features:
            # print("dict:", feature)
            feat = Feature.model_validate(feature)
            print("model", feat)
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
    assert response.status_code == 200
    assert response.json() == {
        "orange": {"2G": True, "3G": False, "4G": True},
        "sfr": {"2G": True, "3G": False, "4G": True},
        "free": {"2G": True, "3G": False, "4G": True},
        "bouygue": {"2G": True, "3G": False, "4G": True},
    }
