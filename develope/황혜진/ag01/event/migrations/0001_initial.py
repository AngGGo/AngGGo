# Generated by Django 5.1.3 on 2024-12-03 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aName', models.CharField(max_length=100)),
                ('attendance', models.CharField(max_length=100)),
                ('aDate', models.CharField(max_length=100)),
            ],
        ),
    ]
