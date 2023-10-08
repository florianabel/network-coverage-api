import pandas as pd
import pyproj

def lamber93_to_gps(x, y):
	lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
	wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
	x = 102980
	y = 6847973
	long, lat = pyproj.transform(lambert, wgs84, x, y)
	return long, lat


if __name__ == "__main__":
    coverage_data = pd.read_csv('src/data/network_coverage.csv', delimiter=';')
    coverage_data['gps'] = coverage_data.apply(lambda x: lamber93_to_gps(x['x'], x['y']), axis=1)
    coverage_data['long'] = coverage_data.apply(lambda x: x['gps'][0], axis=1)
    coverage_data['lat'] = coverage_data.apply(lambda x: x['gps'][1], axis=1)
    coverage_data = coverage_data.drop('gps', axis=1)
    coverage_data.to_csv('src/data/network_coverage_gps.csv', sep=';', index=False)
