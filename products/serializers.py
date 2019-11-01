from rest_framework import serializers
from products import models


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes a name field for testing our APIView"""
    class Meta:
        model = models.ProductList
        fields = ('id','product_name', 'product_img_field', 'product_price', 'created_on')
        

    def create(self, validated_data):
        """create and return a new user"""
        # print("hehe",dir(models.ProductList.objects))
        product = models.ProductList.objects.create(
            product_name=validated_data['product_name'],
            product_img_field=validated_data['product_img_field'],
            product_price=validated_data['product_price'],
        )
        return product