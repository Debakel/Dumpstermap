import mercantile
from django.contrib.gis import geos
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from .serializers import *


class DumpsterList(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Dumpster.objects.all()
    serializer_class = DumpsterSerializer

    @action(detail=False, url_path="tiles/(?P<zoom_level>.+)/(?P<x>.+)/(?P<y>.+)")
    def in_tile(self, request, zoom_level, x, y):
        """Returns all entries within the given tile

        For more info about tiles and slippy maps, see https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
        """
        tile = mercantile.Tile(int(x), int(y), int(zoom_level))
        bbox = mercantile.bounds(tile)
        polygon = geos.Polygon.from_bbox(bbox)

        dumpsters = Dumpster.objects.filter(location__within=polygon)
        serializer = DumpsterSerializer(dumpsters, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        url_path="withinbounds/(?P<min_x>.+)/(?P<min_y>.+)/(?P<max_x>.+)/(?P<max_y>.+)",
    )
    def within_bounds(self, request, min_x, min_y, max_x, max_y):
        """Returns all entries within the given boundary box."""
        bbox = (float(min_x), float(min_y), float(max_x), float(max_y))
        polygon = geos.Polygon.from_bbox(bbox)

        dumpsters = Dumpster.objects.filter(location__within=polygon)
        serializer = DumpsterSerializer(dumpsters, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        url_path="countwithinbounds/(?P<min_x>.+)/(?P<min_y>.+)/(?P<max_x>.+)/(?P<max_y>.+)",
    )
    def count_within_bounds(self, request, min_x, min_y, max_x, max_y):
        """Returns number of entries within the given boundary box."""
        bbox = (float(min_x), float(min_y), float(max_x), float(max_y))
        polygon = geos.Polygon.from_bbox(bbox)

        dumpsters = Dumpster.objects.filter(location__within=polygon)
        return Response({"count": dumpsters.count()})


class VotingViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Voting.objects.all()[:10]
    serializer_class = VotingSerializer
