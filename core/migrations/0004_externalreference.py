# Generated by Django 3.2.4 on 2021-08-24 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_sharepointexcelfile_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=64)),
                ('sourcekey', models.CharField(max_length=128)),
                ('avgregisterline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.avgregisterline')),
            ],
        ),
    ]
