# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Nomenclature, LSI

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password1)
                return redirect('login')
            else:
                return render(request, 'accounts/register.html', {'error': 'Пользователь с таким именем или email уже существует.'})
        else:
            return render(request, 'accounts/register.html', {'error': 'Пароли не совпадают.'})
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Неверное имя пользователя или пароль.'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    nomenclatures = Nomenclature.objects.all()
    lsis = LSI.objects.all()
    return render(request, 'accounts/home.html', {'nomenclatures': nomenclatures, 'lsis': lsis})

@login_required
def nomenclature_create(request):
    if request.method == 'POST':
        abbreviation = request.POST['abbreviation']
        short_name = request.POST['short_name']
        full_name = request.POST['full_name']
        internal_code = request.POST['internal_code']
        cipher = request.POST['cipher']
        ekps_code = request.POST['ekps_code']
        kvt_code = request.POST['kvt_code']
        drawing_number = request.POST['drawing_number']
        nomenclature_type = request.POST['nomenclature_type']
        Nomenclature.objects.create(
            abbreviation=abbreviation,
            short_name=short_name,
            full_name=full_name,
            internal_code=internal_code,
            cipher=cipher,
            ekps_code=ekps_code,
            kvt_code=kvt_code,
            drawing_number=drawing_number,
            nomenclature_type=nomenclature_type
        )
        return redirect('home')
    return render(request, 'accounts/nomenclature_form.html')

@login_required
def nomenclature_update(request, pk):
    nomenclature = get_object_or_404(Nomenclature, pk=pk)
    if request.method == 'POST':
        nomenclature.abbreviation = request.POST['abbreviation']
        nomenclature.short_name = request.POST['short_name']
        nomenclature.full_name = request.POST['full_name']
        nomenclature.internal_code = request.POST['internal_code']
        nomenclature.cipher = request.POST['cipher']
        nomenclature.ekps_code = request.POST['ekps_code']
        nomenclature.kvt_code = request.POST['kvt_code']
        nomenclature.drawing_number = request.POST['drawing_number']
        nomenclature.nomenclature_type = request.POST['nomenclature_type']
        nomenclature.save()
        return redirect('home')
    return render(request, 'accounts/nomenclature_form.html', {'nomenclature': nomenclature})

@login_required
def nomenclature_delete(request, pk):
    nomenclature = get_object_or_404(Nomenclature, pk=pk)
    if request.method == 'POST':
        nomenclature.delete()
        return redirect('home')
    return render(request, 'accounts/nomenclature_confirm_delete.html', {'nomenclature': nomenclature})

@login_required
def lsi_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        LSI.objects.create(name=name, description=description)
        return redirect('home')
    return render(request, 'accounts/lsi_form.html')

@login_required
def lsi_update(request, pk):
    lsi = get_object_or_404(LSI, pk=pk)
    if request.method == 'POST':
        lsi.name = request.POST['name']
        lsi.description = request.POST['description']
        lsi.save()
        return redirect('home')
    return render(request, 'accounts/lsi_form.html', {'lsi': lsi})

@login_required
def lsi_delete(request, pk):
    lsi = get_object_or_404(LSI, pk=pk)
    if request.method == 'POST':
        lsi.delete()
        return redirect('home')
    return render(request, 'accounts/lsi_confirm_delete.html', {'lsi': lsi})
