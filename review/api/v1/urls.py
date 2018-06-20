from django.urls import include, path
from rest_framework_nested import routers

from review.api.v1.views import CompanyViewSet, ReviewViewSet


router = routers.SimpleRouter()
router.register(r'company', CompanyViewSet, base_name='company')
router.register(r'review', ReviewViewSet, base_name='review')

reviews_router = routers.NestedSimpleRouter(router, r'company', lookup='company')
reviews_router.register(r'review', ReviewViewSet, base_name='company-review')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
]