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

from E_commerce.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET

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
    return render(request, 'signup.html')


client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def mens_main(request):
    amount = 5000
    order_curr = 'INR'
    
    order_id = client.order.create(dict(amount=amount,currency=order_curr,payment_capture = 1))

    context ={
        'amount' : amount,
        'api_key' : RAZOR_KEY_ID,
        'order_id' : order_id['id'],
    }
    # return render(request, 'new_try.html', context)
    return render(request, 'mens_main.html',context)

def women_main(request):
    return render(request, 'women_main.html')

def kids_main(request):
    return render(request, 'kids_main.html')

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id','')
            razorpay_order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 5000  # Rs. 200
                try:
 
                    # capture the payemt
                    client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponse("Problem here")
    else:
       # if other than POST request is made.
        return HttpResponse("This is it")
