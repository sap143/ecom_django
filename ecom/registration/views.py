from django.shortcuts import render, redirect
from .forms import RegistrationForm, MFATokenForm, LoginForm, ChangePasswordForm
from django.http import JsonResponse
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
import base64
from django_otp.util import random_hex
from .models import CustomUser
from django.urls import reverse
import qrcode
from io import BytesIO
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
        
            if password != confirm_password:
                print("not mactegd")
                messages.error(request, "Passwords do not match. Please try again.")
                return render(request, 'registration/register.html', {'form': form})
            
            # Check if the username or email already exists
            if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Username or email already exists. Please choose a different one.")
                return render(request, 'registration/register.html', {'form': form})

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        secret_key = random_hex(20)

        device = TOTPDevice.objects.create(
            user=user,  # Assuming 'user' is the registered user
            confirmed=False,
            key=secret_key

        )
        user.save()
        print(device)
        print(type(device))
        # Generate the provisioning URL for setting up MFA
        # provisioning_url = device.config_url()
        provisioning_url = device.config_url
        messages.success(request, "Registration successful. You can now log in.")
        request.session['provisioning_url'] = provisioning_url
        request.session['username'] = username
        return redirect('mfa_setup')

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})



def verify_otp(request):
    print("veridation donde")
    return JsonResponse({"data":"otp verification success"})


def mfa_setup(request):
    # Assuming you've passed the provisioning URL in the context
    # provisioning_url = request.GET.get('provisioning_url')  # Get the provisioning URL
    provisioning_url = request.session.get('provisioning_url')
    username = request.session.get('username')
    print("username ", username)
    print("mfa setup view provisioning url ", provisioning_url)


    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to base64
    buffer = BytesIO()
    img.save(buffer)
    image_data = buffer.getvalue()
    base64_image = "data:image/png;base64," + base64.b64encode(image_data).decode('utf-8')

    if request.method == 'POST':
        # Assuming you have a form to handle MFA setup
        form = MFATokenForm(request.POST)
        if form.is_valid():
            # Process form submission (e.g., save MFA token)
            user = CustomUser.objects.get(username=username)
            totp_device = TOTPDevice.objects.get(user=user)

        # Verify the token
            token = form.cleaned_data['MFA_CODE']
            if totp_device.verify_token(token):
            # If token is valid, mark the device as confirmed
                totp_device.confirmed = True
                totp_device.save()

            # Redirect to success page or dashboard
            # return render(request, 'registration/register.html', {'form': form})
            return redirect("index")
    else:
        form = MFATokenForm()
    
    return render(request, 'registration/mfa_setup.html', {'form': form,'provisioning_url': provisioning_url, 'base64_image': base64_image})



def login_with_mfa(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mfa_code = form.cleaned_data['mfa_code']
            print(username)
            print(password)


            # Get the user
            user = CustomUser.objects.get(username='salman')

            # Check the password
            print(user.check_password('123'))  # This should return True


            user = authenticate(request,username=username, password=password)
            if user is not None:
                if user.is_active:
                    print("user is active")
                    # user = CustomUser.objects.get(username=username)
                    totp_device = TOTPDevice.objects.get(user=user)
                    print("totp device")
                    if totp_device.verify_token(mfa_code):
                        login(request, user)
                        print("hello success login")
                        return redirect('index')
                        # return redirect('success_page')  # Replace with your success page URL name
                    else:
                        form.add_error('mfa_code', 'Invalid MFA code. Please try again.')
                else:
                    form.add_error(None, 'This account is not active.')
            else:
                form.add_error('password', 'Invalid username or password.')

    else:
        form = LoginForm()
    return render(request, 'registration/login_with_mfa.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_with_mfa')  # Redirect to your desired page after logout (change 'login' to your URL name)

@login_required(login_url='login_with_mfa')
def change_password_view(request):
    if request.method == 'POST':
        print("resuest ok")
        form = ChangePasswordForm(request.user, request.POST)
        if not form.is_valid():
            print(form.errors)
        if form.is_valid():
            # Check MFA first
            mfa_code = form.cleaned_data['mfa_code']
            print("form is valid")
            # if not TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
            #     return redirect('mfa_setup')  # Redirect to MFA setup if not set up yet
            totp_device = TOTPDevice.objects.get(user=request.user)
            if totp_device.verify_token(mfa_code):
                # return redirect('success_page')  # Replace with your success page URL name
                new_password = form.cleaned_data['new_password2']
                request.user.set_password(new_password)
                request.user.save()
                print("password change ")
                return redirect('logout_view')  # Redirect to login page after password change
            else:
                form.add_error('mfa_code', 'Invalid MFA code. Please try again.')
            # Proceed with password change logi  
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'registration/change_password.html', {'form': form})


def index(request):
    # return render(request,'index.html')
    return redirect('product_list')





