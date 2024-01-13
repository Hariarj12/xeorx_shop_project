from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Order,Customer
from django.db.models import Sum
from django.contrib.auth.models import User
from .forms import BookForm,CustomerForm
from django.contrib import messages
from .forms import AddToCartForm
from django.http import Http404
from decimal import Decimal


#===========================================================================================================================

def confirm_order(request): 
    # Get the cart from session
    cart = request.session.get('cart', {})

    # Calculate the total price and update cart with book details
    total_price = 0
    customers   = []  # To store Customer instances in the cart

    for book_id, item in cart.items(): 
        book = Book.objects.get(pk=book_id)

        # Handle the case when 'total_price' is not present in 'item'
        try: 
            total_price = item['total_price']
        except KeyError: 
            # Calculate 'total_price' using book price and quantity
            total_price = book.price * item['quantity']

        # Create a new Customer instance and set the book field
        customer = Customer.objects.create(
            user        = request.user,     # You may need to adjust this based on your User model
            book        = book,
            quantity    = item['quantity'],
            total_price = total_price,
            name        = 'John Doe'  # Replace with the actual customer name
        )

        customers.append(customer)

    some_data = None  # Define some_data outside the if statement

    if request.method == 'POST':
       form            = CustomerForm(request.POST)
       if form.is_valid(): 
            # Create a new Customer instance
            customer_name = form.cleaned_data['name']
            customer      = Customer.objects.create(name=customer_name)
            
            # Replace the following placeholder functions with your actual logic
            cart        = get_cart_data_somehow()  # Replace with your logic
            total_price = calculate_total_price_somehow()  # Replace with your logic
            some_data   = "your data here"  # Define some_data

            # Redirect to the confirmation page
            return redirect('confirmation_page')  # Adjust the URL name if needed
    else: 
        form = CustomerForm()

    return render(request, 'base/view_cart.html', {'some_data': some_data, 'form': form})



# =========================================================================================================================== 

def view_cart(request): 
    cart         = request.session.get('cart', {})
    total_amount = 0

    for book_id, item in list(cart.items()): 
        try    : 
            book                 = get_object_or_404(Book, pk=book_id)
            item['name']         = book.name
            item['total_price']  = item['quantity'] * book.price
            total_amount        += item['total_price']
        except Book.DoesNotExist: 
            del cart[book_id]

    return render(request, 'base/view_cart.html', {'cart': cart.values(), 'total_amount': total_amount})
# def view_cart(request): 
#     # Retrieve the cart from session
# cart = request.session.get('cart', {})
#     # Calculate the total amount
# total_amount = 0
# for book_id, item in cart.items(): 
# book = get_object_or_404(Book, pk=book_id)
#         total_amount += book.price * item['quantity']

#     return render(request, 'base/view_cart.html', {'cart': cart, 'total_amount': total_amount})
    
# ============================================================================================================================= 


def add_to_cart(request, book_id): 
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
       form            = AddToCartForm(request.POST)
       if form.is_valid(): 
            quantity = form.cleaned_data['quantity']

            # Get or initialize the cart from session
            cart           = request.session.get('cart', {})
            price_as_float = float(book.price)

            # Update the cart with the selected book and quantity
            if book.id in cart: 
                cart[book.id]['quantity'] += quantity
            else: 
                cart[book.id] = {'name': book.name, 'quantity': quantity, 'price': price_as_float}

            # Save the updated cart in session
            request.session['cart'] = cart

            print(f"Book {book.name} added to cart. Updated cart: {cart}")

            # Redirect to customer_book_list
            return redirect('customer_book_list')

    return render(request, 'base/add_to_cart.html', {'book': book, 'form': form})



# def add_to_cart(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)

#     # Get or initialize the cart from session
#     cart = request.session.get('cart', {})
    
#     # Convert Decimal values to float before storing in the session
#     price_as_float = float(book.price)

#     # Update the cart with the selected book and   quantity
#     if book.id in cart:
#         cart[book.id]['quantity'] += 1
#     else:
#         cart[book.id] = {'name': book.name, 'quantity': 1, 'price': price_as_float}

#     # Save the updated cart in session
#     request.session['cart'] = cart

#     print(f"Book {book.name} added to cart. Updated cart: {cart}")

#     return redirect('customer_book_list')



# def add_to_cart(request, book_id):
#     book = Book.objects.get(pk=book_id)

#     if request.method == 'POST':
#         form = AddToCartForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']

#             # Create or update the customer's cart
#             customer = request.user.customer
#             try:
#                 customer_order = customer.orders.get(book=book)
#                 customer_order.quantity += quantity
#                 customer_order.save()
#             except Customer.orders.model.DoesNotExist:
#                 Customer.orders.create(book=book, quantity=quantity)

#             return redirect('cart')
#     else:
#         form = AddToCartForm()

#     return render(request, 'base/add_to_cart.html', {'book': book, 'form': form})
#=============================================================================================================================
def customer_book_list(request): 
    # Retrieve the updated cart from the URL parameters
    cart = request.GET.get('cart', {})

    # Calculate the total book price
    total_price = calculate_total_price(cart)

    # Retrieve the list of available books
    books = Book.objects.all()

    return render(request, 'base/customer_book_list.html', {'books': books, 'cart': cart, 'total_price': total_price})

def calculate_total_price(cart): 
    total_price = Decimal('0.00')  # Use Decimal for precision
    for book_id, item in cart.items(): 
        book         = get_object_or_404(Book, pk=book_id)
        quantity     = item.get('quantity', 0)  # Handle missing 'quantity' key
        total_price += book.price * quantity
    return total_price

# def customer_book_list(request):
#     books = Book.objects.all()
#     return render(request, 'base/customer_book_list.html', {'books': books}) ------>san

#=============================================================================================================================
def user_list_all(request):
    users = User.objects.all()
    return render(request, 'base/user_list_all.html', {'users': users})
#=============================================================================================================================
def user_list(request):
    users_with_orders = User.objects.annotate(total_books_ordered=Sum('order__quantity'))
    return render(request, 'base/user_list.html', {'users_with_orders': users_with_orders})
#=============================================================================================================================
def user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    user_orders = Order.objects.filter(user=user)
    return render(request, 'base/user_detail.html', {'user': user, 'user_orders': user_orders})
#=============================================================================================================================
# def user_list(request):
#     users_with_orders = User.objects.annotate(
#         total_books_ordered=Sum('order__quantity'),
#         total_price=Sum(models.F('order__quantity') * models.F('order__book__price'))
#     )
#     return render(request, 'base/user_list.html', {'users_with_orders': users_with_orders})

# def user_detail(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user_orders = Order.objects.filter(user=user)
#     return render(request, 'base/user_detail.html', {'user': user, 'user_orders': user_orders})
#=============================================================================================================================
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_name = book.name                       # Save the book name before deleting for the warning message
    book.delete()
    
    messages.success(request, f'Book "{book_name}" has been removed.')
    return redirect('book_list')
#=============================================================================================================================
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.name}" has been updated.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'base/edit_book.html', {'form': form, 'book': book})
#=============================================================================================================================

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')        # Redirect to the books list page
    else:
        form = BookForm()

    return render(request, 'base/add_book.html', {'form': form})
#=============================================================================================================================
def book_list(request):
    books = Book.objects.all()
    return render(request, 'base/book_list.html', {'books': books})\
