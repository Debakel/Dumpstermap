from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r"dumpsters", DumpsterList)
router.register(r"votings", VotingViewSet)

urlpatterns = [re_path(r"^", include(router.urls))]
