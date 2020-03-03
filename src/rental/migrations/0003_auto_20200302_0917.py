# Generated by Django 2.2.7 on 2020-03-02 02:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_auto_20200302_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='rent_date',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='che',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='Name does not allow special charecters', regex='^[\\w-]+$')]),
        ),
        migrations.AlterField(
            model_name='kind',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='Name does not allow special charecters', regex='^[\\w-]+$')]),
        ),
    ]