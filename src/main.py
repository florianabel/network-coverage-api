import requests
import pandas as pd

from fastapi import FastAPI
from pydantic import ValidationError

from .models import NetworkCoverage, Feature, ProviderCoverage

coverage_data = pd.read_csv('src/data/network_coverage.csv', delimiter=';')

app = FastAPI()


@app.get("/", response_model_by_alias=True)
async def root(q: str) -> NetworkCoverage:
    features: list[Feature] = []
    response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={q}")
    res_json = response.json()
    if features := res_json.get('features', None):
        for feature in features:
            try:
                feat = Feature.model_validate(feature)
                features.append(feat)
            except ValidationError as e:
                print(e)
    
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
