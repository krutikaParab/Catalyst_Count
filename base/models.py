from django.db import models
from django.contrib.auth.models import AbstractUser
from chunked_upload.models import ChunkedUpload
from django.utils.translation import gettext_lazy as _

# Create your models here.
# Requirements:
# 'User' needs to login
# User will 'Upload' a file
# 'Query builder' will be built based on file data


class User(AbstractUser):
    """User model"""
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Upload(models.Model):
    file = models.FileField(upload_to='files')

    class Meta:
        verbose_name = 'Upload'
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return self.file


FileChunkUpload = ChunkedUpload


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True)
    domain = models.CharField(max_length=225, null=True, blank=True)
    foundationYear = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=225, null=True, blank=True)
    companySize = models.CharField(max_length=225, null=True, blank=True)
    locality = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    currentEmployeeCount = models.IntegerField(null=True, blank=True)
    totalEmployeeCount = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
