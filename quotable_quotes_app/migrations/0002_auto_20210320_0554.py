# Generated by Django 2.2 on 2021-03-20 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotable_quotes_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='quoted_by',
            new_name='quoted',
        ),
    ]
