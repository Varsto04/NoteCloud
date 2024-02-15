# Generated by Django 4.2.5 on 2023-10-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('user1_id', models.IntegerField()),
                ('user2_id', models.IntegerField()),
                ('user3_id', models.IntegerField()),
            ],
        ),
    ]
