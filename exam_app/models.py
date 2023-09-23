from django.db import models
from django.contrib.auth.models import AbstractUser
import qrcode, random
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
import pyqrcode
import png
from pyqrcode import QRCode

ROLE_OF_USERS = (("1","admin"),("2","normal_user"))  #*roles of users*

class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(unique=True,max_length=15, null=True, blank=True) #*phone number should be unique*
    dateofbirth = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    role_of_user = models.CharField(max_length=255, choices=ROLE_OF_USERS, default="1")
    activation_link = models.URLField(null=True, blank=True)
    timestamp = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    product_image = models.ImageField(upload_to="media/", null=True, blank=True)
    cost = models.IntegerField(null=False, blank=False)
    sale_price = models.IntegerField(null=False, blank=False)
    discount = models.IntegerField(null=True, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", null=True, blank=True)
    def save(self,*args,**kwargs):
        # url = f'http://127.0.0.1:8000/qrcode/{self.product_name}/'
        url=f'https://7266-2401-4900-1c6f-6195-dcf6-4fd5-7521-5eae.ngrok-free.app/qrcode/{self.product_name}/'
        # lst = [self.product_name, self.cost, self.sale_price]
        qrcode_img=qrcode.make(url)
        canvas=Image.new("RGB", (1000,3000),"white")
        draw=ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer=BytesIO()
        canvas.save(buffer,"PNG")
        self.qr_code.save(f'image{random.randint(0,9999)}.png',File(buffer),save=False)
        canvas.close()
        super(Product, self).save(*args,**kwargs)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_item = models.ManyToManyField(Product, related_name="products")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)     
    Total_bill = models.IntegerField(default=None)
    purchase_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)