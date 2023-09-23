from . import views
from django.urls import path
from .views import UserRegisterAPI, LogInAPI, ChangePassword, Products, AllProducts, CheckoutApi,ForgotPasswordSign_link,\
                   AllUsersApi, EditPurchaseDetails, DisplayDetail

urlpatterns = [
    path('api/register/', UserRegisterAPI.as_view()),
    path('api/signinapi/', LogInAPI.as_view()),
    path('api/RestPassword/<token>/<identify>/', ChangePassword.as_view()),
    path('api/ForgotPasswordSign/', ForgotPasswordSign_link.as_view()),
    path('api/Products/', Products.as_view()),
    path('api/allproducts/', AllProducts.as_view()),
    path('api/checkout/', CheckoutApi.as_view()),
    path('api/allusers/', AllUsersApi.as_view()),
    path('api/editpurchasedetails/<int:id>/', EditPurchaseDetails.as_view()),
    path('qrcode/<product_name>/', DisplayDetail.as_view()),
]
#https://3ae3-112-196-43-19.ngrok-free.app/qrcode/{self.product_name}/