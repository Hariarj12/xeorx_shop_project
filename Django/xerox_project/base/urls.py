
from django.urls import path
from .views import book_list,add_book, remove_book, edit_book,user_detail, user_list_all,add_to_cart, customer_book_list,view_cart,confirm_order

urlpatterns = [
    path('book_list/', book_list, name='book_list'),
    path('add_book/', add_book, name='add_book'),
    path('remove_book/<int:book_id>/', remove_book, name='remove_book'),
    path('edit-book/<int:book_id>/', edit_book, name='edit_book'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    path('user_list_all/', user_list_all, name='user_list_all'),
    path('customer_book_list/', customer_book_list, name='customer_book_list'),
    path('view_cart/', view_cart, name='view_cart'),
    path('confirm_order/',confirm_order,name='confirm_order'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),

]

