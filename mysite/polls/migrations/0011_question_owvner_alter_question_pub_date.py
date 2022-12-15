# Generated by Django 4.1.3 on 2022-12-09 09:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0010_remove_question_owvner'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='owvner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 12, 35, 15, 879105), verbose_name='date published'),
        ),
    ]
