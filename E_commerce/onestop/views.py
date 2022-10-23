import email
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
# For sending messages
from django.contrib import messages
# For accessing social account model
from allauth.socialaccount.models import SocialAccount

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
