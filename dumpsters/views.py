from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from shapely.geometry import Polygon, box
from shapely.wkt import dumps

from .geo import tilenum2deg
from .serializers import *


class DumpsterList(RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dumpster.objects.all()
    serializer_class = DumpsterSerializer

    @list_route(url_path='tiles/(?P<zoom_level>.+)/(?P<x>.+)/(?P<y>.+)')
    def in_tile(self, request, zoom_level, x, y):
        """Returns all entries within the given tile

        See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames for documentation
        about slippy maps and how to convert Tile numbers to lon./lat."""
        zoom_level = int(zoom_level)
        x = int(x)
        y = int(y)

        lat_top, lng_left = tilenum2deg(x, y, zoom_level)
        lat_bottom, lng_right = tilenum2deg(x + 1, y + 1, zoom_level)
        boundary = Polygon([(lng_left, lat_top), (lng_right, lat_top), (lng_right, lat_bottom), (lng_left, lat_bottom)])
        boundary_wkt = dumps(boundary)

        dumpsters = Dumpster.objects.filter(location__within=boundary_wkt)
        serializer = DumpsterSerializer(dumpsters, many=True)
        return Response(serializer.data)

    @list_route(url_path='withinbounds/(?P<lat_x>.+)/(?P<lng_x>.+)/(?P<lat_y>.+)/(?P<lng_y>.+)')
    def within_bounds(self, request, lat_x, lng_x, lat_y, lng_y):
        """ Returns all dumpster spots within the given boundary box.
        """
        lat_x = float(lat_x)
        lng_x = float(lng_x)
        lat_y = float(lat_y)
        lng_y = float(lng_y)

        boundary = box(lng_x, lat_x, lng_y, lat_y)
        boundary_wkt = dumps(boundary)

        dumpsters = Dumpster.objects.filter(location__within=boundary_wkt)
        serializer = DumpsterSerializer(dumpsters, many=True)
        return Response(serializer.data)

    @list_route(url_path='countwithinbounds/(?P<lat_x>.+)/(?P<lng_x>.+)/(?P<lat_y>.+)/(?P<lng_y>.+)')
    def count_within_bounds(self, request, lat_x, lng_x, lat_y, lng_y):
        """ Returns number of spots within the given boundary box.
        """
        lat_x = float(lat_x)
        lng_x = float(lng_x)
        lat_y = float(lat_y)
        lng_y = float(lng_y)

        boundary = box(lng_x, lat_x, lng_y, lat_y)
        boundary_wkt = dumps(boundary)

        dumpsters = Dumpster.objects.filter(location__within=boundary_wkt)
        return Response({'count': dumpsters.count()})


class VotingViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Voting.objects.all()[:10]
    serializer_class = VotingSerializer
