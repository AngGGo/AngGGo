# Generated by Django 5.1.3 on 2024-12-04 03:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('bno', models.AutoField(primary_key=True, serialize=False)),
                ('btitle', models.CharField(max_length=1000)),
                ('bcontent', models.TextField()),
                ('bgps', models.CharField(max_length=500)),
                ('bgroup', models.IntegerField(null=True)),
                ('bstep', models.IntegerField(default=0)),
                ('bindent', models.IntegerField(default=0)),
                ('bhit', models.IntegerField(default=0)),
                ('bdate', models.DateTimeField(auto_now=True)),
                ('bfile', models.ImageField(blank=True, null=True, upload_to='board')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='member.member')),
            ],
        ),
    ]
