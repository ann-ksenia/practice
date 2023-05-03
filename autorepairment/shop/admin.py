from django.contrib import admin
from django.contrib import messages
from .custom_filters import Active
from .models import *

class OrderInline(admin.StackedInline):
    model = Order
    extra = 1

class AutoInline(admin.StackedInline):
    model = Auto
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'box', 'date', 'master', 'offer', 'cost', 'status',)
    list_display_links = ('id', 'date',)
    search_fields = ('to_find',)
    list_editable = ('status',)
    list_filter = ( Active,'status', 'box', 'date', 'master', 'offer',)


    def save_model(self, request, obj, form, change):
        if not obj.box and (obj.status == "В процессе" or obj.status == "Готово") :
            messages.error(request, 'Добавьте бокс или статус.')
        elif obj.master and not (obj.master == obj.offer.master):
            messages.warning(request, 'Мастер, которого Вы указали, не выполняет эту услугу. Мастер был изменен.')
            obj.save()
        else:
            if obj.status == "В процессе" or obj.status == "Готово":
                if (Order.objects.filter(box = obj.box, status = "Готово").exclude(date = obj.date).count() + \
                        Order.objects.filter(box = obj.box, status = "В процессе").exclude(date = obj.date).count()> 1):
                    messages.warning(request,'Бокс занят. Выберите другой бокс, удалите активные заказы или измените статус.')
                else:
                    obj.save()
            else:
                obj.save()


class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'gos_number','owner','brend')
    list_display_links = ('id', 'gos_number')
    search_fields = ('brend',)
    inlines = [OrderInline, ]
    list_filter = ['owner']


class MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'speciality', 'M_name')
    list_display_links = ('id', 'speciality')
    search_fields = ('M_name',)
    inlines = [OrderInline, ]


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'master')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ['spectr']

    def save_model(self, request, obj, form, change):
        if Offer.objects.filter(title = obj.title).count() > 0:
            messages.error(request, 'Такая услуга уже есть.')
        if obj.master and not obj.master == obj.spectr.master:
            messages.error(request, 'У мастера, которого Вы указали, другой профиль. Мастер был изменен')
            obj.save()
        else:
            obj.save()


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [AutoInline, OrderInline, ]


class OfferSpectrAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display= ('user', 'content', 'date')
    readonly_fields = ('content', 'user')


admin.site.register(Order, OrderAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(OfferSpectr, OfferSpectrAdmin)
admin.site.register(Feedback, FeedbackAdmin)
