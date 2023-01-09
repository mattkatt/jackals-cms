# Generated by Django 4.0.3 on 2022-11-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_eventbooking_character_faction'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='catering_contact_email',
            field=models.EmailField(default='food@test.com', max_length=254),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='catering_name',
            field=models.CharField(default='catering', max_length=250),
        ),
    ]