from django.contrib import admin

from .models import User,Order,OrderDetail,Product,Category

class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','username','is_staff','is_active','otp']


class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','is_available','sequence']
    
class productAdmin(admin.ModelAdmin):
    list_display=['id','name','price','unit','description','is_available','sequence']
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','total','date','status']
    
class OrderDetailAdmin(admin.ModelAdmin):
    list_display=['id','order','product','qty','price']
    

admin.site.register(User,UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,productAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)