# Generated by Django 5.1.3 on 2024-12-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0004_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
