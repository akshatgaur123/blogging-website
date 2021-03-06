# Generated by Django 4.0.4 on 2022-07-05 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_users_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='image_url',
            field=models.CharField(default='https://imgs.search.brave.com/Wmgf1m-wbgzOgdfoZcSGBb5C7baYyA-_V99Okq6dyro/rs:fit:256:225:1/g:ce/aHR0cHM6Ly90c2U0/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5m/TWVtTUdKTklQZDVm/TFRJNlR3SndRSGFI/YSZwaWQ9QXBp', max_length=300),
        ),
        migrations.AddField(
            model_name='users',
            name='image_url',
            field=models.CharField(default='https://imgs.search.brave.com/Wmgf1m-wbgzOgdfoZcSGBb5C7baYyA-_V99Okq6dyro/rs:fit:256:225:1/g:ce/aHR0cHM6Ly90c2U0/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5m/TWVtTUdKTklQZDVm/TFRJNlR3SndRSGFI/YSZwaWQ9QXBp', max_length=300),
        ),
        migrations.AlterField(
            model_name='tags',
            name='child',
            field=models.CharField(default='none', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='history',
            field=models.CharField(default='none', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='preference',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
