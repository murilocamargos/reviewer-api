from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from review.api.v1.serializers import (CompanySerializer, ReviewCompanySerializer,
                                       ReviewSerializer)
from review.models import Company, Review


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Review.objects.filter(reviewer=self.request.user)

        if self.kwargs.get('company_pk'):
            company = get_object_or_404(Company, pk=self.kwargs.get('company_pk'))
            qs = qs.filter(company=company)
        
        return qs.all()
    
    def get_serializer_class(self):
        if self.kwargs.get('company_pk'):
            return ReviewCompanySerializer
        return ReviewSerializer

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def perform_create(self, serializer):
        if self.kwargs.get('company_pk'):
            company = get_object_or_404(Company, pk=self.kwargs.get('company_pk'))
            serializer.save(
                reviewer=self.request.user,
                company=company,
                ip_address=self.get_client_ip(self.request),
            )
        else:
            serializer.save(
                reviewer=self.request.user,
                ip_address=self.get_client_ip(self.request),
            )