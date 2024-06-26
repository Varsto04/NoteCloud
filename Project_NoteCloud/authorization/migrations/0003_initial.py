# Generated by Django 4.2.5 on 2023-10-10 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0002_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(unique=True)),
                ('title', models.TextField()),
                ('content', models.TextField(blank=True, null=True)),
                ('access_label', models.IntegerField()),
                ('user1_id', models.IntegerField(null=True)),
                ('user2_id', models.IntegerField(null=True)),
                ('user3_id', models.IntegerField(null=True)),
            ],
        ),
    ]
