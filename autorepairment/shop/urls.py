from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='home'),
    path('offers/', offers, name='offers'),
    path('discounts/', discounts, name='discounts'),
    path('employee/', employee, name='employee'),
    path('offersspectrs/', offersspectrs, name='offersspectrs'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('spectr/<int:spectr_id>/', offers, name='spectr'),
    path('to_order/', to_order, name='to_order'),
    path('logout/', user_logout, name='logout'),
    path('get_sale/', get_sale, name='get_sale'),
    path('feedback/', feedback, name='feedback')
]
