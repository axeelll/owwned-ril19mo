# Generated by Django 3.1.7 on 2021-03-17 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_auto_20210316_1603'),
        ('history_event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyevent',
            name='asset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='asset.asset'),
            preserve_default=False,
        ),
    ]
