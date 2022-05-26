"""Visualising h3 hexagons and trajectories."""

import geopandas
import h3

from shapely.geometry import Polygon


def polygonise_h3s(h3s):
    """Create a geoseries for a sequence of h3 hexagons."""
    _polygonise = lambda hex_id: Polygon(h3.h3_to_geo_boundary(hex_id, geo_json=True))

    all_polys = geopandas.GeoSeries(
        list(map(_polygonise, h3s)),
        index=h3s,
        crs="EPSG:4326",
    )

    return all_polys
