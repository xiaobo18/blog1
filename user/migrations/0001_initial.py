# Generated by Django 2.0.1 on 2018-01-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('avarta', models.ImageField(max_length=200, upload_to='')),
                ('age', models.IntegerField()),
                ('sex', models.IntegerField()),
            ],
        ),
    ]
