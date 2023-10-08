import pandas as pd
from geopy import distance
import requests

from typing import Optional

from .models import NetworkCoverage, ProviderCoverage

PROVIDER_CODES = {
    "orange": 20801,
    "sfr": 20810,
    "free": 20815,
    "bouygue": 20820,
}

coverage_data = pd.read_csv('src/data/network_coverage_gps.csv', delimiter=';')


def closest_point_provider(df: pd.DataFrame, point: tuple) -> pd.DataFrame:
    df['distance'] = df.apply(
        lambda x: distance.great_circle(
            (x['lat'], x['long']), 
            point,
        ).kilometers,
        axis=1,
    )
    return df[df.distance == df.distance.min()]


def api_call_gouv(q: str) -> Optional[dict]:
    api_url = f"https://api-adresse.data.gouv.fr/search/?q={q}"
    response = requests.get(api_url)
    res_json = response.json()
    features = res_json.get('features', None)
    return features


def gps_to_coverage(gps_coordinates: tuple) -> NetworkCoverage:
    coverage_collection: dict[str, ProviderCoverage] = {}
    for provider, provider_code in PROVIDER_CODES.items():
        df = coverage_data[coverage_data['Operateur'] == provider_code]
        df_closest_point = closest_point_provider(df, gps_coordinates)
        provider_coverage = ProviderCoverage(
            two_g=df_closest_point['2G'] == 1,
            three_g=df_closest_point['3G'] == 1,
            four_g=df_closest_point['4G'] == 1,
        )
        coverage_collection[provider] = provider_coverage
    return NetworkCoverage.model_validate(coverage_collection)
