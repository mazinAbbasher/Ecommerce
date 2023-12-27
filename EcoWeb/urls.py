from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'products',views.ProductViewSet)
router.register(r'orders',views.OrderViewSet)
router.register(r'categories',views.CategoryViewSet)

urlpatterns = [
    path("",include(router.urls)),
    path('verify_otp/', views.verify_otp, name="verify_otp"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('log_out/', views.log_out, name="log_out"),
    path('search_products/<str:query>', views.search_products, name="search_products"),
 ]
