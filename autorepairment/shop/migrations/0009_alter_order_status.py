# Generated by Django 4.1 on 2022-08-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_order_comment_alter_order_status_delete_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('В обработке', 'В обработке'), ('В процессе', 'В процессе'), ('Готово', 'Готово'), ('Закончено', 'Закончено')], default='В обработке', max_length=50, null=True, verbose_name='Статус'),
        ),
    ]
