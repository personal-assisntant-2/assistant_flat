# Generated by Django 3.2.9 on 2021-11-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0002_alter_tag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='note',
            field=models.ManyToManyField(related_name='tags', to='addressbook.Note'),
        ),
    ]
