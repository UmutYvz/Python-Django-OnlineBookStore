# Generated by Django 3.1.7 on 2021-06-02 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('New', 'Yeni'), ('True', 'Evet'), ('False', 'Hayır')], default='True', max_length=10),
        ),
    ]
