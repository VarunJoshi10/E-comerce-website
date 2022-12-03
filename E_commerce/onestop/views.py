import email
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.conf import settings
# For sending messages
from django.contrib import messages
# For accessing social account model
from allauth.socialaccount.models import SocialAccount
# For payment
import razorpay
from django.views.decorators.csrf import csrf_exempt

from .models import Products, Trial, Cart

from E_commerce.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET

# For graphs
from django.views.generic import TemplateView

# Create your views here.


def main(request):
    if request.method == "POST":
        if request.POST.get('btn_name') == 'logout':
            logout(request)
            messages.success(request, "Logout Successfully!")
            return redirect('/')
    else:
        return render(request, 'main.html')

def landing_page(request):      
    if request.method == 'POST':
        if request.POST.get('btn_name') == 'Sign In':
            user_name = request.POST.get('name')
            user_pass = request.POST.get('pass')

            user = authenticate(username = user_name, password = user_pass)

            if user is not None:
                messages.success(request,f'Successfully signed in as {user}.')
                return render(request, 'landing.html',context={'uname':user})
            else:
                messages.error(request,'Please check credentials again')
                return redirect('/')
            
        elif request.POST.get('btn_name') == 'Sign up':
            u_name = request.POST.get('uname')
            u_email = request.POST.get('email')
            u_pass = request.POST.get('pass')

            new_user = User.objects.create_user(u_name,u_email,u_pass)
            new_user.save()

            messages.success(request, 'User created and logged in successfully!!')

            return render(request, 'landing.html',context={'uname':new_user})

        elif request.POST.get('btn_name') == 'go_home':
            return render(request, 'landing.html')
        
    else:
        # Taking details later on taken out the details whichever wanting 
        # user_id is of social account id
        details = SocialAccount.objects.filter(user=request.user).values()
        print(details)
        return render(request, 'landing.html',context={'uname':request.user})



def signup(request):
    # if request.method == 'POST':
    #     pass

    # Add unique constraint here for username  (check for the username if already exists then ask to change it)
    return render(request, 'signup.html')


razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def mens_main(request):
    mens_products = Products.objects.all().filter(category='Mens')

    context = {
        'mens_products' : mens_products
    }

    if request.method == "POST":
        btn_name  = request.POST.get("btn")

        if btn_name == 'Add to Cart':
            product_id = request.POST.get("pid")

            product_details = Products.objects.filter(product_id=product_id).values()[0]

            # Make a alert here if same product is already present in the cart by the same user
            # Use messages 

            cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                image = product_details['image'], title = product_details['name'], 
                desc = product_details['description'], price = product_details['price'])
            cart_obj.save()

    return render(request, 'mens_main.html',context)

def women_main(request):
    women_products = Products.objects.all().filter(category='Women')

    context = {
        'women_products' : women_products
    }
    
    if request.method == "POST":
        btn_name  = request.POST.get("btn")

        if btn_name == 'Add to Cart':
            product_id = request.POST.get("pid")

            product_details = Products.objects.filter(product_id=product_id).values()[0]

            # Make a alert here if same product is already present in the cart by the same user
            # Use messages 

            cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                image = product_details['image'], title = product_details['name'], 
                desc = product_details['description'], price = product_details['price'])
            cart_obj.save()


    return render(request, 'women_main.html',context)

def kids_main(request):
    kids_products = Products.objects.all().filter(category='Kids')

    context = {
        'kids_products' : kids_products
    }

    if request.method == "POST":
        btn_name  = request.POST.get("btn")

        if btn_name == 'Add to Cart':
            product_id = request.POST.get("pid")
            
            product_details = Products.objects.filter(product_id=product_id).values()[0]

            # Make a alert here if same product is already present in the cart by the same user
            # Use messages 

            cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                image = product_details['image'], title = product_details['name'], 
                desc = product_details['description'], price = product_details['price'])
            cart_obj.save()

    return render(request, 'kids_main.html', context)


def regis(request):
    return render(request, 'regis.html')


def payment(request):
    currency = 'INR'
    amount = 20000  # Rs. 200 Get it from user
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment_try.html', context)


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse("This will be the faliure page")
            else:
 
                # if signature verification fails.
                return HttpResponse("This will be the faliure page")
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponse("This will be the faliure page")
    else:
       # if other than POST request is made.
        return HttpResponse("This will be the faliure page")

def graph(request):
    m_products = Products.objects.filter(category = 'Mens').count()

    w_products = Products.objects.filter(category = 'Women').count()

    k_proucts =Products.objects.filter(category = 'Kids').count()

    doghnut_data = {
        'Mens' : m_products,
        'Women' : w_products,
        'Kids' : k_proucts,
    }

    bar_data = Trial.objects.all().distinct()

    context = {
        'data' : bar_data,
        'doghnut_data' : doghnut_data
    }

    return render(request, 'graph_try.html', context)


def trial(request):
    if request.method == 'POST':
        values = request.POST.getlist('val')

        print(values)

        return redirect('/')
    return render(request, 'new_try.html')


def cart(request):
    cart = Cart.objects.filter(user_id = request.user.id).values()

    context = {
        'cart' : cart
    }

    print(cart)
    return render(request, 'cart.html', context)