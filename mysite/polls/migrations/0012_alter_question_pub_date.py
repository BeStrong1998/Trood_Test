# Generated by Django 4.1.3 on 2022-12-09 09:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_question_owvner_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 12, 39, 11, 713371), verbose_name='date published'),
        ),
    ]
