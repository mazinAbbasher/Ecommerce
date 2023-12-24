from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User,Order,OrderDetail,Product,Category


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [ 'email', 'username','password', 'is_staff', 'is_active',"otp"] 
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'







class OrderListSerializer(ModelSerializer):
    details = OrderDetailSerializer(source="orderdetail_set",many=True)
    class Meta:
        model = Order
        fields = '__all__'