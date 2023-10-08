import requests
from typing import Union
from fastapi import FastAPI, HTTPException, Response
from pydantic import ValidationError

from .models import NetworkCoverage, Feature, ProviderCoverage
from .utils import (
    closest_point_orange,
    closest_point_sfr,
    closest_point_free,
    closest_point_bouygue,
)

app = FastAPI()


@app.get("/", response_model_by_alias=True)
async def network_coverage(q: str) -> Union[NetworkCoverage, bool]:
    response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={q}")
    res_json = response.json()
    features = res_json.get('features', None)
    if features and len(features) > 0 :
        try:
            feature_obj = Feature.model_validate(features[0])
        except ValidationError as e:
            print(e)
            raise
        gps_coordinates = feature_obj.geometry.coordinates
        df_closest_point_orange = closest_point_orange(tuple(gps_coordinates))
        df_closest_point_sfr = closest_point_sfr(tuple(gps_coordinates))
        df_closest_point_free = closest_point_free(tuple(gps_coordinates))
        df_closest_point_bouygue = closest_point_bouygue(tuple(gps_coordinates))
       
        provider_data_orange = ProviderCoverage(
            two_g=df_closest_point_orange['2G'] == 1,
            three_g=df_closest_point_orange['3G'] == 1,
            four_g=df_closest_point_orange['4G'] == 1,
        )
        provider_data_sfr = ProviderCoverage(
            two_g=df_closest_point_sfr['2G'] == 1,
            three_g=df_closest_point_sfr['3G'] == 1,
            four_g=df_closest_point_sfr['4G'] == 1,
        )
        provider_data_free = ProviderCoverage(
            two_g=df_closest_point_free['2G'] == 1,
            three_g=df_closest_point_free['3G'] == 1,
            four_g=df_closest_point_free['4G'] == 1,
        )
        provider_data_bouygue = ProviderCoverage(
            two_g=df_closest_point_bouygue['2G'] == 1,
            three_g=df_closest_point_bouygue['3G'] == 1,
            four_g=df_closest_point_bouygue['4G'] == 1,
        )
        coverage = NetworkCoverage(
            orange=provider_data_orange,
            sfr=provider_data_sfr,
            free=provider_data_free,
            bouygue=provider_data_bouygue,
        )
        return coverage
    return HTTPException(status_code=204)
