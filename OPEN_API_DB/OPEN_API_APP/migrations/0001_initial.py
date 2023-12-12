# Generated by Django 4.1.13 on 2023-12-11 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PDF_fields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('email_id', models.CharField(max_length=100)),
                ('mob_no', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=1000)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('speaking_languages', models.CharField(blank=True, max_length=100, null=True)),
                ('d_o_b', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]