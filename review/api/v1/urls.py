from django.urls import include, path
from rest_framework import routers

from review.api.v1.views import CompanyViewSet


router = routers.SimpleRouter()
router.register(r'company', CompanyViewSet, base_name='companies')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]