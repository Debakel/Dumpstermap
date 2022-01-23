import math


def tilenum2deg(x: float, y: float, zoom: int):
    """Returns the coordinates of a slippy map tile

    * Returns the NW-corner of the square
    * Use with x+1 and/or y+1 to get the other corners.
    * With x+0.5 & y+0.5 it will return the center of the tile.

    See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    """
    n = 2.0 ** zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg
