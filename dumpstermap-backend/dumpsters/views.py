from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, mixins
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from shapely.geometry import Polygon
from shapely.wkt import dumps, loads

from .models import Dumpster, Voting
from .serializers import *
from .geo import tilenum2deg


class DumpsterList(RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dumpster.objects.all()
    serializer_class = DumpsterSerializer

    @list_route(url_path='tiles/(?P<zoom_level>.+)/(?P<x>.+)/(?P<y>.+)')
    def in_tile(self, request, zoom_level, x, y):
        ''' See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames for documentation
        about slippy maps and how to convert Tile numbers to lon./lat. '''
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


class VotingViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Voting.objects.all()[:10]
    serializer_class = VotingSerializer