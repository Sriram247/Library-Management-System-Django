# Generated by Django 5.1.2 on 2024-12-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0007_rename_written_book_and_authors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=100)),
                ('change_type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
