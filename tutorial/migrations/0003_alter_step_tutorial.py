# Generated by Django 3.2.19 on 2023-06-16 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_auto_20230616_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='tutorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='tutorial.tutorial'),
        ),
    ]