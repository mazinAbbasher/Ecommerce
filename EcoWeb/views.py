from rest_framework.decorators import api_view
from rest_framework.viewsets import  ModelViewSet
from EcoWeb.tasks import send_otp_email
from .models import User,Order,OrderDetail,Product,Category
from .serializers import OrderListSerializer, UserSerializer,OrderSerializer,OrderDetailSerializer,ProductSerializer,CategorySerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from random import randint
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        
        try:
            email = data["email"]
        except:
            return Response({"message":"email is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            password = data["password"]
        except:
            return Response({"message":"password is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            username= data["username"]
        except:
            return Response({"message":"username is required"},status=status.HTTP_400_BAD_REQUEST)
        otp = randint(1000,9999)
        mydata = {
            "email" : email,
            "password" : password,
            "username": username,
            "otp" : otp
        }
        serializer = self.get_serializer(data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp_email.delay(email, otp)
        return Response({"message":"succes"}, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.action=="create":
            permission_classes= [permissions.AllowAny()]
        else:
            permission_classes= [permissions.IsAdminUser()]
        return permission_classes


@api_view(["POST"])
def verify_otp(request):
    try :
        otp = int(request.data['otp'])
    except:
        return Response({"message":"otp is required"},status=status.HTTP_400_BAD_REQUEST)
    try :
        email = request.data['email']
    except:
        return Response({"message":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except:
        return Response({"message":"not found"},status=status.HTTP_400_BAD_REQUEST)
    if user.otp != otp:
        return Response({"message":"wrong otp"},status=status.HTTP_403_FORBIDDEN)
    else:
        user.is_active = True
        user.save()
        try:
            token = Token.objects.create(user=user)
        except:
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)



        return Response({"message":"success","token":str(token)},status=status.HTTP_200_OK)


@api_view(["POST"])
def sign_in(request):
    data = request.data
    try:
        email = data["email"]
    except:
            return Response({"message":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        password = data["password"]
    except:
        return Response({"message":"password is required"},status=status.HTTP_400_BAD_REQUEST)
   
    user = User.objects.get(email=email)
    if user is None:
            return Response({"message": "No User exist"},status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        try:
            Token.objects.get(user=user).delete()
        except:
            return Response({"message":"unverified email"},status=status.HTTP_403_FORBIDDEN)
        token = Token.objects.create(user=user)
        user.is_active=True
        user.save()
        return Response({"message":"success","token":str(token)},status=status.HTTP_200_OK)

    else :
        return Response({"message":"wrong password"},status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def log_out(request):
    user= request.user
    user.is_active = False
    user.save()
    return Response({"message":"success"},status=status.HTTP_200_OK)
 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by("sequence")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["list",'retrieve']:
            permission_classes= [permissions.AllowAny()]
        else:
            permission_classes= [permissions.IsAdminUser()]
        return permission_classes


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all().order_by("sequence")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # print (instance)
        products = Product.objects.filter(category=instance)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["list",'retrieve']:
            permission_classes= [permissions.AllowAny()]
        else:
            permission_classes= [permissions.IsAdminUser()]
        return permission_classes


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

    def create(self,request):
        total = 0
        data = request.data
        if len(data) == 0 :
            return Response({"message":"no data"},status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=request.user,status=1)
        for detail in data:
            product_id = detail["product_id"]
            qty = detail["qty"]
            
            try:
                product_price = Product.objects.get(id=product_id).price
            except:
                return  Response({f"message":"bad request, product with id {product_id} is not defined"},status=status.HTTP_400_BAD_REQUEST)
            
            price = qty * product_price
            total +=price

            mydata={
                "order":order.id,
                "product":product_id,
                "qty":qty,
                "price":price
            }
            serializer = OrderDetailSerializer(data=mydata)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        order.total = total
        order.save()
        return Response({"message":"success"},status=status.HTTP_201_CREATED)
     
    
    def retrieve(self,request,*args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user :
            return Response({"message":"permission denied"},status=status.HTTP_401_UNAUTHORIZED)
        order = OrderSerializer(instance)
        details = OrderDetail.objects.filter(order=instance)
        serializer = OrderDetailSerializer(details,many = True)
        return Response({"message":"success","order":order.data,"details":serializer.data},status=status.HTTP_200_OK)
        
 
    def list(self,request,*args, **kwargs):
        if request.user.is_staff:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=request.user)
        orders = OrderListSerializer(queryset,many=True)
        return Response({"message":"success","data":orders.data},status=status.HTTP_200_OK)
        

    def destroy(self,request,*args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user or instance.user.is_staff:
            instance.is_deleted = True
            instance.save()
            return Response({"message":"success"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)


    def get_permissions(self):
        if self.action in ["put","patch"]:
            permission_classes= [permissions.IsAdminUser()]
        else:
            permission_classes= [permissions.IsAuthenticated()]
        return permission_classes
