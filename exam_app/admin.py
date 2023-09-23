from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Purchase

fields = list(UserAdmin.fieldsets)
fields[0] = (None,{'fields':('phone_number','password')})
fields[1] = ('Personal Details',{'fields':('full_name','email','dateofbirth')})
UserAdmin.fieldsets = tuple(fields)

class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Address Details',{'fields':('city','state','zipcode')}),
        ('Role of User',{'fields':('role_of_user',)}),
        ('Verification Status',{'fields':('activation_link','timestamp','is_verified')})
    )
    list_display = ('phone_number', 'full_name', 'email','role_of_user')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'cost', 'sale_price')

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'purchaseditems', 'Total_bill', 'purchase_date')   
    def purchaseditems(self, obj):
        return ', '.join([i.product_name for i in obj.purchased_item.all()])   

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)    
admin.site.register(Purchase, PurchaseAdmin)