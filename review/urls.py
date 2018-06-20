from django.urls import include, path


urlpatterns = [
    path('api/v1/', include('review.api.v1.urls')),
]