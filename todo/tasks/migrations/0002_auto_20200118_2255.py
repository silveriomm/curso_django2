# Generated by Django 3.0.2 on 2020-01-19 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='done',
            field=models.CharField(choices=[('doing', 'Doing'), ('done', 'Done')], max_length=5),
        ),
    ]
