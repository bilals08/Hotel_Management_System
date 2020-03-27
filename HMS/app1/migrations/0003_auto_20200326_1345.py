# Generated by Django 3.0.3 on 2020-03-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('service_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('service_type', models.CharField(max_length=15)),
                ('service_desc', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='rooms',
            name='capacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='floor',
            field=models.IntegerField(),
        ),
    ]
