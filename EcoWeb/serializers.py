from rest_framework.serializers import ModelSerializer
from .models import User,Order,OrderDetail,Product,Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'username', 'is_staff', 'is_active',"otp"] 



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