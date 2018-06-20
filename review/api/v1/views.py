import re

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from review.api.v1.serializers import CompanySerializer
from review.models import Company


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]