from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import rest_framework

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer
    
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is a similar to a traiditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URL\'s',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        """handle updating an object"""
        return Response({'method':'PUT'})
    
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})
    

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses action (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message':'Hello!', 'a_viewset':a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})
    
    def update(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Delete an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, rest_framework.permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email',)
    

class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES




class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """View for the Product Category"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateProduct,
        IsAuthenticated
    )
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_staff:
            self.perform_create(serializer)
        else:
            raise PermissionDenied('User is not  Staff')

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # print("hehe", self.request.user.email)
        serializer.save()

class ProductListViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateProduct,
        IsAuthenticated
    )
    serializer_class = serializers.ProductSerializer
    queryset = models.ProductList.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_staff:
            self.perform_create(serializer)
        else:
            raise PermissionDenied('User is not  Staff')

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # print("hehe", self.request.user.email)
        serializer.save()

    