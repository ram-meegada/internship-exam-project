from .models import User, Product, Purchase
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_number','full_name','email','dateofbirth','state','city','zipcode',
                  'password','role_of_user']
        extra_kwargs = {"password":{"write_only":True}, "email":{"required": True}, "role_of_user":{"default":"2"}}

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "product_name", "product_image", "cost", "sale_price","discount","qr_code"]
        extra_kwargs = {"qr_code":{"read_only":True}}   
 
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'purchased_item', 'address_line1','address_line2', 'Total_bill','purchase_date']

class EditPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id','user','purchased_item', 'address_line1','address_line2', 'Total_bill']
        extra_kwargs = {"user":{"read_only":True}}