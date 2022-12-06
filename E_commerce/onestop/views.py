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

from .models import Products, Cart, PaymentDetails, SellerSales

from E_commerce.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET

from django.db.models import Sum, Count

import datetime

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
                title = product_details['name'], 
                price = product_details['price'],
                category = product_details['category'],
                sub_category = product_details['sub_category'])
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
                title = product_details['name'], 
                price = product_details['price'],
                category = product_details['category'],
                sub_category = product_details['sub_category'])
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
                title = product_details['name'], 
                price = product_details['price'],
                category = product_details['category'],
                sub_category = product_details['sub_category'])
            cart_obj.save()

    return render(request, 'kids_main.html', context)


def regis(request):
    return render(request, 'snippets.html')


def graph(request):
    # General items
    m_products = Products.objects.filter(listedBy = 1002 ,category = 'Mens').count()

    w_products = Products.objects.filter(listedBy = 1002 ,category = 'Women').count()

    k_proucts =Products.objects.filter(listedBy = 1002 ,category = 'Kids').count()

    total_products = Products.objects.filter(listedBy = 1002).count()

    summer_products = Products.objects.filter(listedBy = 1002,sub_category = 'Summer').count()
    winter_products = Products.objects.filter(listedBy = 1002,sub_category = 'Winter').count()

    total_sales = SellerSales.objects.filter(sellerId = 1002).aggregate(Sum('sales'))['sales__sum']

    sales_in_months = SellerSales.objects.filter(sellerId = 1002).values('month').annotate(the__count=Count('month'))


    # Summer items
    m_products_summer = Products.objects.filter(listedBy = 1002 ,category = 'Mens', sub_category = 'Summer').count()

    w_products_summer = Products.objects.filter(listedBy = 1002 ,category = 'Women', sub_category = 'Summer').count()

    k_proucts_summer =Products.objects.filter(listedBy = 1002 ,category = 'Kids', sub_category = 'Summer').count()

    total_products_summer = Products.objects.filter(listedBy = 1002,sub_category = 'Summer' ).count()

    total_sales_summer = SellerSales.objects.filter(sellerId = 1002,sub_category = 'Summer').aggregate(Sum('sales'))['sales__sum']

    sales_in_months_summer = SellerSales.objects.filter(sellerId = 1002 , sub_category = 'Summer').values('month').annotate(the__count=Count('month'))


    # Summer winter
    m_products_winter = Products.objects.filter(listedBy = 1002 ,category = 'Mens', sub_category = 'Winter').count()

    w_products_winter = Products.objects.filter(listedBy = 1002 ,category = 'Women', sub_category = 'Winter').count()

    k_proucts_winter =Products.objects.filter(listedBy = 1002 ,category = 'Kids', sub_category = 'Winter').count()

    total_products_winter = Products.objects.filter(listedBy = 1002,sub_category = 'Winter' ).count()

    total_sales_winter = SellerSales.objects.filter(sellerId = 1002,sub_category = 'Winter').aggregate(Sum('sales'))['sales__sum']

    sales_in_months_winter = SellerSales.objects.filter(sellerId = 1002 , sub_category = 'Winter').values('month').annotate(the__count=Count('month'))

    doghnut_data_all = {
        'Mens' : m_products,
        'Women' : w_products,
        'Kids' : k_proucts,
    }

    doghnut_data_summer = {
        'Mens' : m_products_summer,
        'Women' : w_products_summer,
        'Kids' : k_proucts_summer,
    }

    doghnut_data_winter = {
        'Mens' : m_products_winter,
        'Women' : w_products_winter,
        'Kids' : k_proucts_winter,
    }

    context = {
        'doghnut_data_all' : doghnut_data_all,
        'total_products': total_products,
        'winter_products' : winter_products,
        'summer_products' : summer_products,
        'total_sales': total_sales,
        'sales' : sales_in_months,

        'doghnut_data_summer' : doghnut_data_summer,
        'total_products_summer': total_products_summer,
        'total_sales_summer': total_sales_summer,
        'sales_summer' : sales_in_months_summer,

        'doghnut_data_winter' : doghnut_data_winter,
        'total_products_winter': total_products_winter,
        'total_sales_winter': total_sales_winter,
        'sales_winter' : sales_in_months_winter,
    }

    return render(request, 'graph_try.html', context)


# Created razorpay client object by passing id and secret key 
razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


def cart(request):
    cart = Cart.objects.filter(user_id = request.user.id).values()

    if len(cart) != 0:
        total_price = Cart.objects.filter(user_id = request.user.id).aggregate(Sum('price'))['price__sum']

        currency = 'INR'
        amount = total_price * 100
        
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

        # Adding the cart items to the page
        context['cart'] = cart

        store_payment = PaymentDetails(Seller_id = 1001, Customer_id = request.user.id,
            Order_id = razorpay_order_id, Payment_id = '', Signature = '',
            Amount = amount, Month = datetime.datetime.now().month)
        
        store_payment.save()

        return render(request, 'cart.html', context)
    
    else:
        return render(request, 'empty_cart.html')


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
            
            order_details = PaymentDetails.objects.get(Order_id = razorpay_order_id)

            order_details.Signature = signature
            order_details.Payment_id = payment_id
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                
                amount = order_details.Amount
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    order_details.Status = 'Success'
                    order_details.save()

                    sellers = Cart.objects.filter(user_id = order_details.Customer_id).values('listedBy','category','sub_category').annotate(the__sum = Sum('price'))

                    for i in sellers:
                        seller = SellerSales(sellerId = i['listedBy'], sales = i['the__sum'], category = i['category'],
                            sub_category = i['sub_category'], month = order_details.Month) 
                        seller.save()

                    cart_obj = Cart.objects.filter(user_id = order_details.Customer_id).delete()
 
                    # render success page on successful caputre of payment
                    return render(request, 'payment_success.html')
                except:
                    order_details.Status = 'Falied'
                    order_details.save()
                    # if there is an error while capturing payment.
                    return render(request,'payment_fail.html')
            else:
                order_details.Status = 'Failed'
                order_details.save()
                # if signature verification fails.
                return render(request,'payment_fail.html')
        except:
            # if we don't find the required parameters in POST data
            return render(request,'payment_fail.html')
    else:
       # if other than POST request is made.
        return render(request,'payment_fail.html')
    


def sellerLogin(request):
    if request.method == 'POST':
        btn_name = request.POST.get('btn')

        if btn_name == 'Sign up':

            

            return render(request, 'seller_profile.html')
        
        elif btn_name == 'Log in':
            return render(request, 'seller_profile.html')
    return render(request, 'seller_signup.html')

def customerProfile(request):
    return render(request, 'customer_profile.html')

def sellerProfile(request):

    return render(request, 'seller_profile.html')

def pr(request):
    return render(request, 'pr1.html')


def mainSellerProfile(request):
    return render(request, 'seller_main_profile.html')