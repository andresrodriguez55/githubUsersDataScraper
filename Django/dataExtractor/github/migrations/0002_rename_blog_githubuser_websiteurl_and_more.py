# Generated by Django 4.0.2 on 2022-03-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='githubuser',
            old_name='blog',
            new_name='websiteURL',
        ),
        migrations.AddField(
            model_name='githubuser',
            name='followersCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='forksObtained',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='languageMostUsed',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='profilePictureURL',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='repositoriesCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='starsObtained',
            field=models.IntegerField(default=0),
        ),
    ]