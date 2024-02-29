from django.contrib import admin
from .models import Bus, User, Book, Registration, Contact, Refund

# Register your models here.

admin.site.register(User)

class bus_admin(admin.ModelAdmin):
        list_display=('id','bus_name','source','dest','nos','rem','price','date','time')
admin.site.register(Bus,bus_admin)

class book_admin(admin.ModelAdmin):
        list_display=('email','name','userid','busid','bus_name','source','dest','nos','price','date','time','status')
admin.site.register(Book,book_admin)

class register_admin(admin.ModelAdmin):
        list_display=('name','email','age','phone','amount','order_id','paid')
admin.site.register(Registration,register_admin)

class contact_admin(admin.ModelAdmin):
        list_display=('name','email','message')
admin.site.register(Contact,contact_admin)

class refund_admin(admin.ModelAdmin):
        list_display=('username','busname','source','destination','nofseats','price','date','time','refundprice','status')
admin.site.register(Refund,refund_admin)

