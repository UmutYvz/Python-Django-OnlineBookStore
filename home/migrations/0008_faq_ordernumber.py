# Generated by Django 3.1.7 on 2021-06-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210615_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='ordernumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]