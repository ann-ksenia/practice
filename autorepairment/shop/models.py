from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата', blank = True)
    problem = models.TextField(blank=False, verbose_name='Проблема')
    comment = models.TextField(verbose_name='Комментарий', blank = True)
    master = models.ForeignKey('Master', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Мастер')
    client = models.ForeignKey('Client', on_delete=models.PROTECT, null=True, blank = False, verbose_name='Заказчик')
    auto = models.ForeignKey('Auto', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Авто')
    box = models.ForeignKey('Box', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Бокс')
    offer = models.ForeignKey('Offer', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Услуга')
    discount = models.IntegerField(null=True, blank = True, verbose_name='Скидка')
    cost = models.IntegerField(null=True, blank = True, verbose_name='Цена',editable=False)
    to_find = models.CharField(blank = True, default = '__', max_length=200, editable= False)

    def tofind(self):
        if self.offer and self.auto:
            self.to_find = self.client.name + ' ' + self.offer.title +' '+self.auto.gos_number + ' '+ self.auto.brend
        elif self.offer:
            self.to_find = self.client.name + ' ' + self.offer.title
        elif self.auto:
            self.to_find = self.client.name + ' ' + self.auto.gos_number+' '+self.auto.brend

    st1 = 'В обработке'
    st2 = 'В процессе'
    st3 = 'Готово'
    st4 = 'Закончено'
    YEAR_IN_SCHOOL_CHOICES = [
        (st1, 'В обработке'),
        (st2, 'В процессе'),
        (st3, 'Готово'),
        (st4, 'Закончено'),
    ]
    status = models.CharField('Статус',
        max_length=50,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=st1,
        null=True
    )

    def active(self):
        return Order.objects.filter(box = self.box, status = "Готово")+\
                    Order.objects.filter(box = self.box, status = "В процессе")

    def save(self, *args, **kwargs):
        self.tofind()
        self.set_cost()
        self.set_master()
        self.set_client()
        if self.status == "В процессе" or self.status == "Готово":
            if (Order.objects.filter(box = self.box, status = "Готово").exclude(date = self.date).count()+\
                    Order.objects.filter(box = self.box, status = "В процессе").exclude(date = self.date).count() > 1):
                pass
            else:
                super(Order, self).save(*args, **kwargs)
        else:
            super(Order, self).save(*args, **kwargs)

    def set_cost(self):
        if self.discount and self.offer:
            cost = self.offer.price*(1-self.discount/100)
        elif self.offer:
            cost = self.offer.price
            if Order.objects.filter(client = self.client):
                self.discount = 10
        else:
            cost = None
        self.cost = cost

    def set_master(self):
        if self.offer:
            self.master = self.offer.master

    def set_client(self):
        if self.auto:
            self.client = self.auto.owner

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-date']


class Box(models.Model):
    number = models.CharField(max_length=150,null=True, verbose_name='Номер бокса')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=12, null=True, verbose_name='Номер телефона')

    def short_name(self):
        res = ""
        num = 0
        for i in self.name:
            if i == ' ':
                num = 1
            elif num ==1:
                res += i
                num = 0
            else:
                res += i
        return res


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"
        ordering = ['name']


class Master(models.Model):
    speciality = models.CharField(max_length=150, verbose_name='Профиль')
    M_name = models.CharField(max_length=150, verbose_name='ФИО')
    box = models.ForeignKey('Box', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Бокс')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.speciality+' '+self.M_name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастеры"
        ordering = ['M_name']


class Auto(models.Model):
    gos_number = models.CharField(max_length=20,null=True, blank = False, verbose_name='Гос номер')
    owner = models.ForeignKey('Client', on_delete=models.PROTECT, null=True, verbose_name='Владелец')
    brend = models.CharField(max_length=150, verbose_name='Марка', null = True, blank = False)
    year = models.CharField(max_length=150, verbose_name='Год выпуска')
    vin_number = models.IntegerField(null=True, verbose_name='ВИН')

    def __str__(self):
        res = ""
        num = 1
        for i in self.owner.name:
            if i == ' ':
                num = 2
                res += i
            elif num == 2:
                res += i
                res += ". "
                num = 0
            elif num == 0:
                pass
            else:
                res += i
        return res+', '+self.brend+', '+str(self.gos_number)

    class Meta:
        verbose_name = "Авто"
        verbose_name_plural = "Авто"
        ordering = ['owner']


class Offer(models.Model):
    master = models.ForeignKey('Master', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Мастер')
    price = models.IntegerField(null=True, verbose_name='Цена', blank = False)
    title = models.CharField(max_length=150, verbose_name='Услуга')
    spectr = models.ForeignKey('OfferSpectr', on_delete=models.PROTECT, null=True, verbose_name='Спектр услуг')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['title']

    def save(self, *args, **kwargs):
        if Offer.objects.filter(title=self.title).count()>0 :
            pass
        else:
            self.set_master()
            super(Offer, self).save(*args, **kwargs)

    def set_master(self):
        self.master = self.spectr.master



class OfferSpectr(models.Model):
    title = models.CharField(max_length=150, verbose_name='Услуга')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    master = models.ForeignKey('Master', on_delete=models.PROTECT, null=True, blank = True, verbose_name='Мастер')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Спектр услуг"
        verbose_name_plural = "Спектры услуг"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('spectr', kwargs={'spectr_id': self.pk})

class Feedback(models.Model):
    content = models.TextField(verbose_name='Отзыв', )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата', blank = True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank= True, verbose_name='Автор')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-date']


