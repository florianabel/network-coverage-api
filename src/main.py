import requests
from typing import Union
from fastapi import FastAPI, HTTPException, Response
from pydantic import ValidationError

from .models import NetworkCoverage, Feature, ProviderCoverage
from .utils import (
    api_call_gouv,
    gps_to_coverage,
)

app = FastAPI()


@app.get("/", response_model_by_alias=True)
async def network_coverage(q: str) -> Union[NetworkCoverage, bool]:
    features = api_call_gouv(q)
    if features and len(features) > 0 :
        try:
            feature_obj = Feature.model_validate(features[0])
        except ValidationError as e:
            print(e)
            raise
        return gps_to_coverage(feature_obj.geometry.coordinates)
    return HTTPException(status_code=204)
