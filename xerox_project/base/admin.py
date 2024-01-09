from django.contrib import admin


# Register your models here.
from .models import Book
from .models import Order
from .models import Customer

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Customer)
