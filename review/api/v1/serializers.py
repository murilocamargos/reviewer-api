from rest_framework import serializers, validators

from review import models


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = models.Company
        fields = ('id', 'name', )


class ReviewCompanySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    summary = serializers.CharField(max_length=10000)
    ip_address = serializers.IPAddressField(read_only=True)
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.Review
        fields = ('id', 'title', 'rating', 'summary', 'ip_address', 'company',\
            'reviewer')


class ReviewSerializer(ReviewCompanySerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=models.Company.objects.all(),
        many=False,
        read_only=False,
    )