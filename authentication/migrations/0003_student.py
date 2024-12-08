# Generated by Django 5.1.2 on 2024-12-06 09:40

import django.db.models.deletion
import utils.util_functions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(db_index=True, default=utils.util_functions.generate_uuid, max_length=300, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('INTERN', 'INTERN'), ('EXTERN', 'EXTERN'), ('TRIPTERN', 'TRIPTERN')], max_length=300)),
                ('payment_plan', models.CharField(choices=[('FULL', 'FULL'), ('PART', 'PART'), ('NOT PAID', 'NOT PAID')], max_length=30)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='students', to='authentication.program')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
