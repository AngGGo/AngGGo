# Generated by Django 5.1.3 on 2024-12-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_comment_cgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cgroup',
            field=models.IntegerField(null=True),
        ),
    ]
