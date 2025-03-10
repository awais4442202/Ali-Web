from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, Order
import json
from django.http import JsonResponse
from .forms import DeliveryForm
from django.contrib import messages
from .forms import ContactForm
from django.db.models import Q  # For complex queries

def search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []  # Search in name and description

    return render(request, 'search_results.html', {'query': query, 'results': results})


def remove_from_cart_ajax(request, product_id):
    if request.method == "POST":
        # Assuming you have a session-based cart or cart object logic
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Product not found in cart.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# Add product to the cart (using cookies)
def add_to_cart_cookie(request, product_id):
    cart = json.loads(request.COOKIES.get('cart', '{}'))  # Load existing cart data or use an empty dict
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity for the product
    response = JsonResponse({'message': 'Product added to cart successfully!'})
    response.set_cookie('cart', json.dumps(cart), max_age=7 * 24 * 60 * 60)  # Save updated cart in cookies (7 days)
    return response


# Display cart page
def cart_page_cookie(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))  # Load cart data from cookies
    products = Product.objects.filter(id__in=cart.keys())  # Fetch products in the cart
    cart_items = [{'product': product, 'quantity': cart[str(product.id)]} for product in products]
    return render(request, 'cart.html', {'cart_items': cart_items})



# Remove product from cart
def remove_from_cart_cookie(request, product_id):
    if request.method == "POST":  # Ensure it's a POST request
        # Load cart data from cookies
        cart = json.loads(request.COOKIES.get('cart', '{}'))  
        
        # Check if the product exists in the cart
        if str(product_id) in cart:
            del cart[str(product_id)]  # Remove the product from the cart
            
            # Prepare response
            response = JsonResponse({'success': True, 'message': 'Product removed from cart successfully!'})
            
            # Update the cart in cookies
            response.set_cookie('cart', json.dumps(cart), max_age=7 * 24 * 60 * 60)  
            return response
        else:
            return JsonResponse({'success': False, 'error': 'Product not found in cart.'})
    
    # If not a POST request, return an error
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_page')



def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})



def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the same page or a 'thank you' page
    else:
        form = ContactForm()
    featured_products = Product.objects.order_by('-views')[:8]
    return render(request, 'home.html', {'form': form, 'featured_products': featured_products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



def shop(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})






# Add product to the wishlist (cookie-based)

def add_to_wishlist_cookie(request, product_id):
    # Retrieve the existing wishlist from cookies, defaulting to an empty list
    raw_cookie = request.COOKIES.get('wishlist', '[]')
    try:
        wishlist = json.loads(raw_cookie)  # Parse existing wishlist JSON
    except json.JSONDecodeError:
        wishlist = []  # If parsing fails, reset to an empty list

    # Add the new product to the wishlist if it's not already there
    if product_id not in wishlist:
        wishlist.append(product_id)

    # Save the updated wishlist back to the cookie
    response = JsonResponse({'message': 'Product added to wishlist successfully!'})
    response.set_cookie('wishlist', json.dumps(wishlist), max_age=7 * 24 * 60 * 60)  # 7 days expiry

    return response


# Remove product from the wishlist (cookie-based)
def remove_from_wishlist_cookie(request, product_id):
    if request.method == "POST":
        try:
            # Load wishlist as a list from cookies
            wishlist = json.loads(request.COOKIES.get('wishlist', '[]'))  # Parse wishlist as a list

            # Ensure the ID exists in the list
            if int(product_id) in wishlist:  # Convert to int for comparison
                wishlist.remove(int(product_id))  # Remove the product ID

                # Send response and update the cookie
                response = JsonResponse({"success": True})
                response.set_cookie('wishlist', json.dumps(wishlist), max_age=7 * 24 * 60 * 60)  # 7 days expiry
                return response

            # If the product ID is not found
            return JsonResponse({"error": "Item not found in wishlist."}, status=404)
        except Exception as e:
            # Handle any parsing or processing errors
            return JsonResponse({"error": str(e)}, status=400)
    # Handle invalid request method
    return JsonResponse({"error": "Invalid request method."}, status=400)





def wishlist_page_cookie(request):
    raw_cookie = request.COOKIES.get('wishlist', '[]')
    try:
        wishlist = json.loads(raw_cookie)  # Parse existing wishlist JSON
    except json.JSONDecodeError:
        wishlist = []  # If parsing fails, reset to an empty list

    # Fetch the products from the database
    products = Product.objects.filter(id__in=wishlist)

    return render(request, 'wishlist.html', {'products': products})








# Buy Page
from django.shortcuts import redirect

def buy_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = DeliveryForm(request.POST)

        if form.is_valid():
            # Create the order
            order = Order.objects.create(
                user=None,  # Assuming guest user, modify if you're using authenticated users
                product=product,
                quantity=1,  # Assuming single quantity for now
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
            )
            
            # Redirect to the success page, passing the order ID
            return redirect('purchase_success', order_id=order.id)

        else:
            # Handle form errors
            print(f"Form Errors: {form.errors}")

    else:
        form = DeliveryForm()

    return render(request, 'buy.html', {'product': product, 'form': form})



# Success Page
def purchase_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'purchase_success.html', {'order': order})





def checkout(request):
    # Retrieve cart items from cookies
    cart = request.COOKIES.get('cart')
    cart_items = []

    if cart:
        cart = json.loads(cart)
        for product_id, details in cart.items():
            product = get_object_or_404(Product, id=product_id)
            cart_items.append({
                'product': product,
                'quantity': details['quantity']
            })

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            # Create orders for each cart item
            for item in cart_items:
                Order.objects.create(
                    user=None,  # Guest order
                    product=item['product'],
                    quantity=item['quantity'],
                    address=form.cleaned_data['address'],
                    phone_number=form.cleaned_data['phone_number']
                )
            
            # Clear the cart after successful checkout
            response = redirect('purchase_success')
            response.delete_cookie('cart')
            messages.success(request, "Your order has been placed successfully!")
            return response
    else:
        form = DeliveryForm()

    return render(request, 'checkout.html', {'cart_items': cart_items, 'form': form})


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message to the database
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to the same contact page or another page after submission
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

