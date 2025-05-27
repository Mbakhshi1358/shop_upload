from django.shortcuts import render , redirect , reverse , get_object_or_404
from django.utils.crypto import get_random_string
from django.views import View
from .forms import LoginForm ,RegisterForm , OtpCheckForm
from .models import Otp , User
from django.contrib.auth import authenticate, login, logout
import random

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"account/login.html",{'form':form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None :
                login(request, user)
                return redirect("/")
        return render(request,"account/login.html",{'form':form})


class RegisterView(View):
    def get(self,request):
        form =  RegisterForm()
        return render(request,"account/register.html",{"form":form})
    def post(self,request):
        form =  RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = random.randint(1111,9999)
            token = get_random_string(length=155)
            Otp.objects.create(phone=cd['phone'] , code=code , token=token)
            print(code)
            return redirect(reverse("account:checkotp") + F"?token={token}")

        return render(request, "account/register.html", {"form": form})

class OtpCheckView(View):
    def get(self,request):
        form = OtpCheckForm()
        return render(request, "account/otp_check.html",{'form':form} )
    def post(self,request):
        token = request.GET.get('token')
        form = OtpCheckForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp=Otp.objects.get(token = token)
                user = User.objects.create_user(phone=otp.phone)
                otp.delete()
                login(request, user)
                return redirect("/")
        return render(request, "account/otp_check.html", {'form': form})




def LogoutUser(request):
    logout(request)
    return redirect("/")