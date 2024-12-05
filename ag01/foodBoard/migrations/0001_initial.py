# Generated by Django 5.1.3 on 2024-12-02 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board_f',
            fields=[
                ('bNo', models.AutoField(primary_key=True, serialize=False)),
                ('bTitle', models.CharField(max_length=200)),
                ('bContent', models.TextField(max_length=2000)),
                ('bFile', models.FileField(upload_to='Board_f')),
                ('bHit', models.IntegerField(default=0, max_length=100)),
                ('bLike', models.IntegerField(default=0, max_length=100)),
                ('bDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
