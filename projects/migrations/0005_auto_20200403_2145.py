# Generated by Django 2.2 on 2020-04-03 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200123_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='manager_status',
            field=models.IntegerField(choices=[(0, 'проект'), (1, 'в работе'), (2, 'окончен'), (3, 'отменен')], default=0, verbose_name='Статус проекта'),
        ),
    ]
