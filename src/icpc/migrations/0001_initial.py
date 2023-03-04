# Generated by Django 4.1.7 on 2023-03-04 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('id_number', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('country_of_origin', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.ManyToManyField(to='icpc.participant')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.CharField(choices=[('LO', 'Local'), ('NA', 'National'), ('RE', 'Regional'), ('IN', 'International')], max_length=2)),
                ('year', models.IntegerField()),
                ('score', models.IntegerField()),
                ('team', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='icpc.team')),
            ],
        ),
    ]
