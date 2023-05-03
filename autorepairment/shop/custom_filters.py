from django.contrib.admin import SimpleListFilter
from django.db.models import Q

class Active(SimpleListFilter):
    title = 'Активные заказы'
    parameter_name = 'Active orders'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Активные'),
            ('not_active', 'Неактивные')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        elif self.value().lower() == 'active':
            return queryset.all().exclude(status = 'В обработке').exclude(status = 'Закончено')
        elif self.value().lower() == 'not_active':
            return queryset.all().exclude(status = 'Готово').exclude(status = 'В процессе')