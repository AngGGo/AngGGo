# Generated by Django 5.1.3 on 2024-12-02 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='아이디')),
                ('pw', models.CharField(max_length=100, verbose_name='패스워드')),
                ('name', models.CharField(max_length=100, verbose_name='사용자명')),
                ('nickname', models.CharField(max_length=100, verbose_name='닉네임')),
                ('birth', models.DateField(null=True, verbose_name='생년월일')),
                ('email', models.EmailField(max_length=100, verbose_name='사용자이메일')),
                ('tel', models.CharField(default='010-0000-0000', max_length=20)),
                ('point', models.IntegerField(default=0, verbose_name='마일리지')),
                ('agree1', models.DateTimeField(auto_now=True, verbose_name='필수약관동의')),
                ('agree2', models.DateTimeField(auto_now=True, verbose_name='선택약관동의')),
                ('mDate', models.DateTimeField(auto_now=True, verbose_name='가입일')),
            ],
        ),
    ]
