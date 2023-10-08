from pydantic import BaseModel, ConfigDict, Field, conlist
from typing import Optional, Literal, Union


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