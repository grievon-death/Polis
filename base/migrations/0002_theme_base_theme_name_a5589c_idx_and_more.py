# Generated by Django 5.0.6 on 2024-06-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='theme',
            index=models.Index(fields=['-name'], name='base_theme_name_a5589c_idx'),
        ),
        migrations.AddIndex(
            model_name='type',
            index=models.Index(fields=['name'], name='base_type_name_661789_idx'),
        ),
    ]
