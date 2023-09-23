from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegistrationSerializer, AddProductSerializer, PurchaseSerializer,\
                        EditPurchaseSerializer
from django.contrib.auth.hashers import make_password, check_password
from . models import User, Product, Purchase
import pyqrcode, qrcode
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .helper import resetpwdlink, send_activation_link
from django.core.files.base import ContentFile

#*Class based view for user registration*
class UserRegisterAPI(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        password = request.data['password']
        request.data['password'] = make_password(password)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            send_activation_link(serialized_data)
            if serialized_data["role_of_user"] == "1":
                item = User.objects.get(phone_number=serialized_data["phone_number"])
                item.is_superuser = True
                item.is_staff = True
                item.save()
            return Response({"data":serialized_data, "message":"Registration Succesfully done"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogInAPI(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        password= request.data['password']
        try:
            user= User.objects.get(phone_number=phone_number)
            check_pwd =  check_password(password,user.password)
            if check_pwd:
                token = RefreshToken.for_user(user)
                data = {"user_mobilenumber":user.phone_number,"access_token":str(token.access_token),"refresh_token":str(token), "message":
"you are successfully logged in"}
                return Response(data)
            elif not check_pwd:
                data = {"message":"wrong password"}
                return Response(data)
        except:
            data = {"user":"no user found"}
            return Response(data)    
        
#* using authorization token *
# class ChangePassword(APIView): 
#     permission_classes = [IsAuthenticated]   #*changing password with token only*
#     serializer_class = UserRegistrationSerializer
#     def post(self, request):
#         phone_number = request.data['phone_number']
#         current_password = request.data['current_password']
#         New_password = request.data['New_password']    
#         Confirm_Newpassword = request.data['Confirm_Newpassword']   
#         item = User.objects.filter(phone_number=phone_number)
#         if not item:
#             data = {"message": "mobile number not found. Please try again"}
#             return Response(data)
#         elif not check_password(current_password, item[0].password):
#             data = {"message": "Old password is not correct"}
#             return Response(data)
#         elif New_password != Confirm_Newpassword:
#             data = {"message":"newpasword and confirm new password are not matching"}
#             return Response(data)
#         elif New_password == Confirm_Newpassword:
#             item[0].password = make_password(New_password)
#             item[0].save()
#             serializer = self.serializer_class(item[0])
#             serialized_data = serializer.data
#             return Response({"data": serialized_data, "message": "Password successfully updated"}, status=status.HTTP_201_CREATED) 
        

class ForgotPasswordSign_link(APIView):
    def post(self, request):
        email = request.data['email']
        item = User.objects.filter(email=email)
        if item:
            resetpwdlink(item)
            data = {"message":"Forgot your password? Don't worry we will send you reset passsword link to your registered email"}
            return Response(data)
        elif not item:
            data = {"message":"Email not found. Please try again"}
            return Response(data)
            
class ChangePassword(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request,token, identify):
        current_password = request.data['current_password']
        New_password = request.data['New_password']    
        Confirm_Newpassword = request.data['Confirm_Newpassword']   
        item = User.objects.filter(email=identify)
        if not item:
            data = {"message": "user not found. Please try again"}
            return Response(data)
        elif not check_password(current_password, item[0].password):
            data = {"message": "Old password is not correct"}
            return Response(data)
        elif New_password != Confirm_Newpassword:
            data = {"message":"newpasword and confirm new password are not matching"}
            return Response(data)
        elif New_password == Confirm_Newpassword:
            item[0].password = make_password(New_password)
            item[0].save()
            serializer = self.serializer_class(item[0])
            serialized_data = serializer.data
            return Response({"data": serialized_data, "message": "Password successfully updated"}, status=status.HTTP_201_CREATED) 
              
# class Products(APIView):
#     serializer_class = AddProductSerializer
#     permission_classes = [IsAdminUser]     # *Admin can only add products*
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             # serializer.save()
#             serialized_data = serializer.data
#             return Response({"data":serialized_data, "message":"Product Added"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Products(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddProductSerializer
    def post(self, request):
        product_name = request.data["product_name"]
        product_image = request.data["product_image"]
        cost = request.data["cost"]
        sale_price = request.data["sale_price"]
        discount = request.data["discount"]
        try:
            item = Product.objects.get(product_name=product_name)
            message = "Same name products can't be entered."
            return Response({"Caution":message}, status=status.HTTP_400_BAD_REQUEST)
        except:
            obj = Product.objects.create(product_name=product_name,product_image=product_image,cost=cost,sale_price=sale_price,discount=discount)
            serializer = self.serializer_class(obj)
            serilaized_data = serializer.data
            data = {"data":serilaized_data,"message":"added"}
            return Response(data)

class AllProducts(APIView):
    serializer_class = AddProductSerializer
    def get(self, request):
        items = Product.objects.all()
        a = items.values()
        print(type(a), "=========================")
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        print(type(serialized_data),"====================")
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class CheckoutApi(APIView):
    serializer_class = PurchaseSerializer
    def post(self, request):
        user = request.data['user']
        purchased_items = request.data['purchased_item']
        address_line1 = request.data['address_line1']  
        address_line2 = request.data['address_line2']
        total = 0
        for i in purchased_items:
            total += Product.objects.get(id=i).sale_price
        pur_item = Purchase.objects.create(user_id=user ,address_line1=address_line1, 
                                           address_line2=address_line2, Total_bill=total)
        record = Purchase.objects.get(id = pur_item.id)
        record.purchased_item.add(*purchased_items)
        serializer = self.serializer_class(record)
        serilaized_data = serializer.data
        return Response({"shipping_details":serilaized_data}, status=status.HTTP_201_CREATED)
    
class AllUsersApi(APIView):
    serializer_class = UserRegistrationSerializer
    def get(self,request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class EditPurchaseDetails(APIView):
    serializer_class = EditPurchaseSerializer
    def put(self, request,id):
        purchase_obj = Purchase.objects.get(id=id)
        serializer = self.serializer_class(purchase_obj, data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisplayDetail(APIView):
    serializer_class = AddProductSerializer
    def get(self, request, product_name):
        item = Product.objects.get(product_name=product_name)
        serializer = self.serializer_class(item)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
