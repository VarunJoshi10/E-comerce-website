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

from .models import Products, Cart, PaymentDetails, SellerSales, Seller, currSeller, OrderStatus

from E_commerce.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET

# Q for complex queries
from django.db.models import Sum, Count, Q

import datetime

# For image uploading from html page
from django.core.files.storage import FileSystemStorage


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
            try:
                u_name = request.POST.get('uname')
                u_email = request.POST.get('email')
                u_pass = request.POST.get('pass')

                new_user = User.objects.create_user(u_name,u_email,u_pass,first_name = u_name)
                new_user.save()

                messages.success(request, 'User created and logged in successfully!!')

                return redirect('/')
            except:
                messages.error(request, 'Please change username')

                return render(request, 'signup.html')


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
    if request.POST.get('btn_name') == 'Sign up':
        try:
            u_name = request.POST.get('uname')
            u_email = request.POST.get('email')
            u_pass = request.POST.get('pass')

            new_user = User.objects.create_user(u_name,u_email,u_pass)
            new_user.save()

            messages.success(request, 'User created and logged in successfully!!')

            return redirect('/')
        except:
            messages.error(request, 'Please change username')

            return render(request, 'signup.html')

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

            product_ids = Cart.objects.filter(user_id = request.user.id, prod_id = product_id)

            if len(product_ids) != 0:
                messages.error(request, "Item already in cart")
            else:
                product_details = Products.objects.filter(product_id=product_id).values()[0] 

                cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                    title = product_details['name'], 
                    price = product_details['price'],
                    category = product_details['category'],
                    sub_category = product_details['sub_category'])
                cart_obj.save()

                messages.success(request, "Item Added to cart")

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

            product_ids = Cart.objects.filter(user_id = request.user.id, prod_id = product_id)

            if len(product_ids) != 0:
                messages.error(request, "Item already in cart")
            else:
                product_details = Products.objects.filter(product_id=product_id).values()[0]


                cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                    title = product_details['name'], 
                    price = product_details['price'],
                    category = product_details['category'],
                    sub_category = product_details['sub_category'])
                cart_obj.save()

                messages.success(request, "Item added to cart")

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

            product_ids = Cart.objects.filter(user_id = request.user.id, prod_id = product_id)

            if len(product_ids) != 0:
                messages.error(request, "Item already in cart")
            else:
                product_details = Products.objects.filter(product_id=product_id).values()[0]

                cart_obj = Cart(user_id=request.user.id, prod_id = product_id,listedBy = product_details['listedBy'], 
                    title = product_details['name'], 
                    price = product_details['price'],
                    category = product_details['category'],
                    sub_category = product_details['sub_category'])
                cart_obj.save()

                messages.success(request, "Item added to cart")

    return render(request, 'kids_main.html', context)


def graph(request):

    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    # General items
    m_products = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Mens').count()

    w_products = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Women').count()

    k_proucts =Products.objects.filter(listedBy = seller_obj.Id ,category = 'Kids').count()

    total_products = Products.objects.filter(listedBy = seller_obj.Id).count()

    summer_products = Products.objects.filter(listedBy = seller_obj.Id,sub_category = 'Summer').count()
    winter_products = Products.objects.filter(listedBy = seller_obj.Id,sub_category = 'Winter').count()

    total_sales = SellerSales.objects.filter(sellerId = seller_obj.Id).aggregate(Sum('sales'))['sales__sum']

    sales_in_months = SellerSales.objects.filter(sellerId = seller_obj.Id).values('month').annotate(the__count=Count('month'))


    # Summer items
    m_products_summer = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Mens', sub_category = 'Summer').count()

    w_products_summer = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Women', sub_category = 'Summer').count()

    k_proucts_summer =Products.objects.filter(listedBy = seller_obj.Id ,category = 'Kids', sub_category = 'Summer').count()

    total_products_summer = Products.objects.filter(listedBy = seller_obj.Id,sub_category = 'Summer' ).count()

    total_sales_summer = SellerSales.objects.filter(sellerId = seller_obj.Id,sub_category = 'Summer').aggregate(Sum('sales'))['sales__sum']

    sales_in_months_summer = SellerSales.objects.filter(sellerId = seller_obj.Id , sub_category = 'Summer').values('month').annotate(the__count=Count('month'))


    # Summer winter
    m_products_winter = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Mens', sub_category = 'Winter').count()

    w_products_winter = Products.objects.filter(listedBy = seller_obj.Id ,category = 'Women', sub_category = 'Winter').count()

    k_proucts_winter =Products.objects.filter(listedBy = seller_obj.Id ,category = 'Kids', sub_category = 'Winter').count()

    total_products_winter = Products.objects.filter(listedBy = seller_obj.Id,sub_category = 'Winter' ).count()

    total_sales_winter = SellerSales.objects.filter(sellerId = seller_obj.Id,sub_category = 'Winter').aggregate(Sum('sales'))['sales__sum']

    sales_in_months_winter = SellerSales.objects.filter(sellerId = seller_obj.Id , sub_category = 'Winter').values('month').annotate(the__count=Count('month'))

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
        'seller_obj' : seller_obj,
    
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
        context['original_price'] = total_price

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

                    cart_obj = Cart.objects.filter(user_id = order_details.Customer_id).values()

                    for i in cart_obj:
                        order = OrderStatus(user_id = i['user_id'], prod_id = i['prod_id'], 
                            listedBy = i['listedBy'],title = i['title'],
                            price = i['price'], category = i['category'],
                            status = 'Packed')
                        order.save() 

                    cart_obj_del = Cart.objects.filter(user_id = order_details.Customer_id).delete()


 
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

            name = request.POST.get("signup_name")
            signup_mob = request.POST.get("signup_mob")
            signup_password = request.POST.get("signup_password")
            store_name = request.POST.get("store_name")

            new_seller = Seller(name = name, password = signup_password, Mobile = signup_mob, ShopName = store_name)
            new_seller.save()

            currSeller_obj = currSeller(s_no = 1, seller_id = new_seller.Id)
            
            currSeller_obj.save()
            
            context = {
                'seller_obj' : new_seller
            }

            return render(request, 'seller_profile.html' , context)
        
        elif btn_name == 'Log in':

            mob = request.POST.get("mob")
            password = request.POST.get("pass")

            seller_obj = Seller.objects.get(Mobile = mob, password = password)
            
            currSeller_obj = currSeller(s_no = 1, seller_id = seller_obj.Id)
            
            currSeller_obj.save()
            
            context = {
                'seller_obj' : seller_obj
            }

            return render(request, 'seller_profile.html', context)
        
        
    return render(request, 'seller_signup.html')

def customerProfile(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout Successfully!!")
        return redirect('/')
    return render(request, 'customer_profile.html')

def sellerProfile(request):          
    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    context = {
                'seller_obj' : seller_obj
            }
    return render(request, 'seller_profile.html', context)

def pr(request):
    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    if seller_obj.VerificationStatus == 'Not Verified':
        context = {
                    'seller_obj' : seller_obj,
                    'content': 'Your verification is not done yet please wait till the time'
                }
        return render(request, 'seller_profile.html', context)

    else:
        context = {
                    'seller_obj' : seller_obj
                }
        
        if request.method == "POST":
            prod_name = request.POST.get('prod_name')
            prod_desc = request.POST.get('prod_desc')
            prod_price = request.POST.get('prod_price')
            prod_category = request.POST.get('category')
            prod_sub_category = request.POST.get('sub_category')
            image = request.FILES.get('upload_img')

            new_prod = Products.objects.create(listedBy = currSeller_obj.seller_id, name = prod_name, price = int(prod_price),
                category = prod_category, sub_category = prod_sub_category, description = prod_desc,
                image = image)
            
            new_prod.save()

            return render(request, 'pr1.html',context)

    return render(request, 'pr1.html',context)


def mainSellerProfile(request):
    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    if request.method == 'POST':         
        currSeller_obj = currSeller.objects.get(s_no = 1)
        
        image = request.FILES.get('upload_img')
        
        seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

        context = {
                'seller_obj' : seller_obj
            }

        if image != None:
            seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)
            seller_obj.VerificationDocument = image

            seller_obj.save()

            messages.success(request, "Document Uploaded Successfully")
            
            context = {
                'seller_obj' : seller_obj
            }

            return render(request, 'seller_main_profile.html', context)
        
        else:
            messages.error(request, "Please upload the document")
            return render(request, 'seller_main_profile.html', context)

    context = {
                'seller_obj' : seller_obj
            }
    return render(request, 'seller_main_profile.html',context)

def sellerLogout(request):
    currSeller.objects.get(s_no = 1).delete()
    return redirect('/sellerLogin')

def viewProduct(request):
    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    product_obj = list(Products.objects.filter(listedBy = seller_obj.Id).values())

    print(product_obj, len(product_obj))

    context = {
                'seller_obj' : seller_obj,
                'product_obj': product_obj
            }
    return render(request, 'seller_products_view.html', context)


def sellerOrders(request):
    currSeller_obj = currSeller.objects.get(s_no = 1) 

    seller_obj = Seller.objects.get(Id = currSeller_obj.seller_id)

    print(currSeller_obj.seller_id)

    if request.method == "POST":
        new_status = request.POST.get('getStatus')
        cust_id = int(request.POST.get('cust_id'))
        prod_i = int(request.POST.get('prod_id'))

        update_status = OrderStatus.objects.get(listedBy = currSeller_obj.seller_id, user_id = cust_id, 
            prod_id = prod_i)
        
        print(new_status, cust_id, prod_i)
        
        if update_status.status == new_status:
            messages.error(request, "Need to change the status fist.")
        else:
            update_status.status = new_status
            update_status.save()
            messages.success(request,"Status of the product is updated.")

    ongoingOrders = OrderStatus.objects.filter(Q(listedBy = currSeller_obj.seller_id) & (Q(status = 'Dispatched') | Q(status = 'Out for Delivery') | Q(status = 'Packed'))).values()
    
    print(len(ongoingOrders))

    context = {
                'seller_obj' : seller_obj,
                'orders' : ongoingOrders
            }


    return render(request, 'SellerOrders.html', context)


def customerOrders(request):
    orders = OrderStatus.objects.filter(user_id = request.user.id).values()

    context = {
        'orders': orders
    }
    return render(request, 'customer_orders.html',context)