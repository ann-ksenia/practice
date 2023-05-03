from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth import login as dj_login, logout
from django.contrib import messages
from django.core.mail import send_mail


def main(request):
    return render(request, 'shop/main.html')


def offersspectrs(request):
    offersspectrs = OfferSpectr.objects.all()
    context = {
        'offersspectrs': offersspectrs
    }
    return render(request, 'shop/offersspectrs.html', context)


def discounts(request):
    return render(request, 'shop/discounts.html')


def employee(request):
    employee = Master.objects.all()
    context = {
        'employee': employee
    }
    return render(request, 'shop/employee.html', context)


def offers(request):
    offers = Offer.objects.all()
    context = {
        'offers': offers
    }
    return render(request, 'shop/offers.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            messages.success(request, 'Успешный вход')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not (Client.objects.filter(phone=user.last_name).count() > 0 and Client.objects.filter(
                    name=user.first_name).count() > 0):
                client = Client()
                client.name = user.first_name
                client.phone = user.last_name
                client.save()
            dj_login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def offers(request, spectr_id):
    offers = Offer.objects.filter(spectr_id=spectr_id)
    spectr = OfferSpectr.objects.get(pk=spectr_id)
    return render(request, 'shop/offers.html', {'offers': offers, 'spectr': spectr})


def user_logout(request):
    logout(request)
    return redirect('login')


def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['topic'], form.cleaned_data['content'], 'ksenia.shestakova.94@mail.ru',
                             ['kns8@tpu.ru'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('register')
            else:
                messages.success(request, 'Письмо ne отправлено')
    else:
        form = ContactForm()
    return render(request, 'shop/register.html', {'form': form})


def get_sale(request):
    if Client.objects.filter(name=request.user.first_name).count() > 0:
        if Order.objects.filter(client=Client.objects.get(name=request.user.first_name)).count() > 5:
            sale = 10
            amount = Order.objects.filter(client=Client.objects.get(name=request.user.first_name)).count()
        else:
            sale = 0
            amount = 0
    else:
        sale = 0
        amount = 0
    return render(request, 'shop/get_sale.html', {'sale': sale, 'amount': amount})


def feedback(request):
    feedbacks = Feedback.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save()
            fb.user = request.user
            fb.save()
            return redirect('feedback')
    if request.user.is_authenticated:
        form = FeedbackForm()
        return render(request, 'shop/feedback.html', {'feedbacks': feedbacks, 'form': form})
    else:
        return render(request, 'shop/feedback.html', {'feedbacks': feedbacks})

def to_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            if Client.objects.filter(name=request.user.first_name).count() > 0:
                order.client = Client.objects.get(name=request.user.first_name)
                order.save()
            return redirect('home')
    if request.user.is_authenticated:
        form = OrderForm()
        return render(request, 'shop/to_order.html', {'form': form})
    else:
        return user_login(request)