# Generated by Django 3.2.9 on 2022-02-24 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habits_managerAPI', '0003_alter_habitfulfillment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitfulfillment',
            name='fulfillment_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fulfillemnts', to='habits_managerAPI.fulfillmentlevel'),
        ),
    ]