from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }

    def create(self, validated_data):
        """create and return a new user"""
        print(self.request)
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """serializes profile feed items"""
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile':{'read_only':True}
        }        
    
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes a Product"""
    class Meta:
        model = models.ProductList
        fields = ('id','product_name', 'product_category', 'product_img_field', 'product_price', 'created_on')


    def create(self, validated_data):
        """create and return a new product"""
        # print("hehe",validated_data.keys())
        product = models.ProductList.objects.create(
            product_name=validated_data['product_name'],
            product_img_field=validated_data['product_img_field'],
            product_price=validated_data['product_price'],
            product_category=validated_data['product_category'],
        )
        return product

class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializes a product category"""
    class Meta:
        model = models.ProductCategory
        fields = ('id', 'product_category')

    def create(self, validated_data):
        """create and return new category"""

        product_category = models.ProductCategory.objects.create(
            product_category = validated_data['product_category'],
        )
        return product_category