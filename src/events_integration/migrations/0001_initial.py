# Generated by Django 3.2.12 on 2022-02-18 18:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('modification_datetime', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('modification_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128)),
                ('sell_mode', models.CharField(editable=False, max_length=32)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('event_datetime', models.DateTimeField()),
                ('sell_from', models.DateTimeField()),
                ('sell_to', models.DateTimeField()),
                ('sold_out', models.BooleanField()),
                ('organizer_company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_events', to='events_integration.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('modification_datetime', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField()),
                ('numbered', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='events_integration.event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
