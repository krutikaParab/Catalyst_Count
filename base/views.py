from django.shortcuts import render, redirect
from .forms import UserForm, UploadForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Company, Upload


def login_user(request):
    page = 'login-user'

    if request.user.is_authenticated:
        return redirect('upload-data')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username or password does not existed")
        except:
            messages.error(request, "User is not existed")
    context = {'page': page}
    return render(request, 'login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login-user')


def register_user(request):
    try:
        page = 'register-user'
        form = UserForm()
        try:
            if request.method == 'POST':
                form = UserForm(request.POST)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.email = user.email.lower()
                    user.save()
                    login(request, user)
                    return redirect('upload-data')

            context = {'form': form}
        except Exception as e:
            messages.error(request, e)

        return render(request, 'login_register.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse("Failed to register user {}".format(e))

@login_required(login_url='login-user/')
def upload_data(request):
    form = UploadForm()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect(reversed('upload-data'))

    context = {'form': form}
    return render(request, 'upload_file.html', context=context)


@login_required(login_url='login-user/')
def query_data(request):
    company = Company.objects.all()
    industry = company.distinct('industry')
    year = company.distinct('foundationYear')
    city = company.distinct('locality')
    country = company.distinct('country')

    context = {
                   'industry': industry,
                   'year': year,
                   'city': city,
                   'country': country
               }
    print(context)
    return render(request, 'company_query.html', context=context)

