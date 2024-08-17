# Generated by Django 4.2.15 on 2024-08-16 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_biometricprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainCruise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_number', models.CharField(blank=True, max_length=20, null=True)),
                ('departure_station', models.CharField(blank=True, max_length=100, null=True)),
                ('arrival_station', models.CharField(blank=True, max_length=100, null=True)),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('arrival_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='trainticket',
            name='arrival_station',
        ),
        migrations.RemoveField(
            model_name='trainticket',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='trainticket',
            name='departure_station',
        ),
        migrations.RemoveField(
            model_name='trainticket',
            name='departure_time',
        ),
        migrations.RemoveField(
            model_name='trainticket',
            name='train_number',
        ),
        migrations.AddField(
            model_name='trainticket',
            name='train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='train', to='users.traincruise'),
        ),
    ]
