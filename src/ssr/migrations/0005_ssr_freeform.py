# Generated by Django 2.2.7 on 2020-03-27 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssr', '0004_auto_20200325_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssr',
            name='freeform',
            field=models.BooleanField(default=False),
        ),
    ]
