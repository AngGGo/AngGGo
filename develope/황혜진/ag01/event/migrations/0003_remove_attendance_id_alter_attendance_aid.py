# Generated by Django 5.1.3 on 2024-12-05 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_rename_aname_attendance_aid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='id',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='aId',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
