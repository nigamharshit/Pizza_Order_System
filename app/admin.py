from django.contrib import admin
from app.models import Pizza,  PizzaBase, Cheese, Topping, Order

# Register your models here.
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

class PizzaBaseAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

class CheeseAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

class ToppingAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','status','total_price')

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(PizzaBase, PizzaBaseAdmin)
admin.site.register(Cheese, CheeseAdmin)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Order, OrderAdmin)