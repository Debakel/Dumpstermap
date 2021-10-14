from django.conf.urls import url, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r"dumpsters", DumpsterList)
router.register(r"votings", VotingViewSet)

urlpatterns = [url(r"^", include(router.urls))]
