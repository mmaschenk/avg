# Generated by Django 3.2.4 on 2021-10-06 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20211004_1052'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='externalreference',
            constraint=models.UniqueConstraint(fields=('source', 'sourcekey'), name='unique_external'),
        ),
    ]