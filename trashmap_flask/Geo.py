import math


#
# Converts Tile numbers to lon./lat. (for slippy maps)
# This returns the NW-corner of the square. Use the function with xtile+1 and/or ytile+1 to get the other corners.
# With xtile+0.5 & ytile+0.5 it will return the center of the tile.
# See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def tilenum2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)
