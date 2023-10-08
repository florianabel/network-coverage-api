import pandas as pd
from geopy import distance

coverage_data = pd.read_csv('src/data/network_coverage_gps.csv', delimiter=';')
coverage_data_orange = coverage_data[coverage_data['Operateur'] == 20801]
coverage_data_sfr = coverage_data[coverage_data['Operateur'] == 20810]
coverage_data_free = coverage_data[coverage_data['Operateur'] == 20815]
coverage_data_bouygue = coverage_data[coverage_data['Operateur'] == 20820]

def closest_point(df: pd.DataFrame, point: tuple) -> pd.DataFrame:
    df['distance'] = df.apply(
        lambda x: distance.great_circle(
            (x['lat'], x['long']), 
            point,
        ).kilometers,
        axis=1,
    )
    return df[df.distance == df.distance.min()]

def closest_point_orange(point: tuple) -> pd.DataFrame:
    return closest_point(coverage_data_orange, point)

def closest_point_sfr(point: tuple) -> pd.DataFrame:
    return closest_point(coverage_data_sfr, point)

def closest_point_free(point: tuple) -> pd.DataFrame:
    return closest_point(coverage_data_free, point)

def closest_point_bouygue(point: tuple) -> pd.DataFrame:
    return closest_point(coverage_data_bouygue, point)