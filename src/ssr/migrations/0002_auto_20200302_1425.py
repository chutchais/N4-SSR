# Generated by Django 2.2.7 on 2020-03-02 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ssr.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ssr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssr',
            name='number',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Ssrfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(upload_to=ssr.models.content_file_name)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('ssr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='ssr.Ssr')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
