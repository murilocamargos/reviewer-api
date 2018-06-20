from django.contrib.auth.models import User
from django.db import models


class TimestampModel(models.Model):
    """
    Abstract model with automatically updated created_at and updated_at fields.

    Attributes:
    <DateTimeField> created_at -- Created date, has auto_now_add.
    <DateTimeField> updated_at -- Updated date, has auto_now.
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        null=False,
        blank=True,
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        null=False,
        blank=True,
        auto_now=True
    )

class Company(TimestampModel):
    """
    Models the company to be reviewed.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"


class Review(TimestampModel):
    title = models.CharField(max_length=64)
    rating = models.IntegerField() # 1-5
    summary = models.CharField(max_length=10000)
    ip_address = models.GenericIPAddressField()
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        super(Review, self).save(*args, **kwargs)