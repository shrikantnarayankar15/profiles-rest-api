from django.shortcuts import render
from products import serializers
from products import models
from profiles_api import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductListViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProductSerializer
    queryset = models.ProductList.objects.all()
    permissions = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    # queryset = models.ProductList.objects.all()
    # print("he",queryset)
    # def perform_create(self, serializer):
    #     """Sets the user profile to the logged in user"""
    #     print(self.request)
    #     serializer.save(name=self.request)